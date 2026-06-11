import datetime
from DB_Manager import DBManager
from Entity.Vacation_Entity import Vacation
from Entity.Employee_Entity import Employee

# 휴가 목록, 승인, 반려 등을 처리하는 컨트롤러
class VacationControl:
    @classmethod
    def get_vacation_list(self):
        print("[VacationControl] DB 데이터를 UI 양식에 맞게 변환 중...")
        # 1. Entity를 통해 DB에서 데이터를 가져옴
        raw_list = Vacation.get_all() 
        formatted_list = []
        
        # 2. 휴가 종류 변환
        type_map = {1: "연차", 2: "반차", 3: "공가", 4: "병가"}
        
        for row in raw_list:
            # 3. 휴가 기간 계산
            start_d = row["start_day"]
            end_d = row["end_day"]
            
            # DB에서 온 날짜가 문자열인지 날짜 객체인지 판별하여 처리
            if isinstance(start_d, str):
                start_obj = datetime.datetime.strptime(start_d, '%Y-%m-%d').date()
                end_obj = datetime.datetime.strptime(end_d, '%Y-%m-%d').date()
            else:
                start_obj = start_d
                end_obj = end_d
                
            duration_days = (end_obj - start_obj).days + 1
            
            # 4. Boundary가 읽을 수 있는 Key 이름으로 딕셔너리 생성
            formatted_vac = {
                "vac_id": row["vac_id"],
                "emp_name": row["emp_name"],
                "dep_name": row["dep_name"],
                "role": "일반직원",
                "status": row["vac_status"],
                "vac_type": type_map.get(row["vac_type_id"], "기타"),
                "start_date": str(start_d),
                "end_date": str(end_d),
                "duration": f"{duration_days}일",
                "reason": row["reason"]
            }
            formatted_list.append(formatted_vac)
            
        return formatted_list

    def approve_vacation(self, vac_id, man_id):
        print(f"[VacationControl] approve_vacation() 실행 -> vac_id: {vac_id}, 결재 관리자: {man_id}")
        
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 승인할 휴가의 상세 정보 조회
                sql_select = "SELECT emp_id, start_day, end_day FROM vacation WHERE vac_id = %s"
                cursor.execute(sql_select, (vac_id,))
                vac_info = cursor.fetchone()
                
                if not vac_info:
                    print("[VacationControl] 존재하지 않는 휴가 신청 건입니다.")
                    return False
                
                emp_id = vac_info["emp_id"]
                start_day = vac_info["start_day"]
                end_day = vac_info["end_day"]
                
                # 2. 시작일과 종료일을 바탕으로 사용한 휴가 일수 계산
                if isinstance(start_day, str):
                    start_obj = datetime.datetime.strptime(start_day, '%Y-%m-%d').date()
                    end_obj = datetime.datetime.strptime(end_day, '%Y-%m-%d').date()
                else:
                    start_obj = start_day
                    end_obj = end_day
                
                use_days = (end_obj - start_obj).days + 1
                
                # 3. 휴가 테이블의 처리 상태와 관리자 ID 반영
                sql_update_vac = """
                    UPDATE vacation 
                    SET vac_status = '승인됨', man_id = %s 
                    WHERE vac_id = %s
                """
                cursor.execute(sql_update_vac, (man_id, vac_id))
                
                # 4. 직원 테이블의 잔여 휴가에서 사용 일수만큼 차감
                sql_update_emp = """
                    UPDATE employee 
                    SET remain_vacation = remain_vacation - %s 
                    WHERE emp_id = %s
                """
                cursor.execute(sql_update_emp, (use_days, emp_id))
                
                # 모든 쿼리가 성공하면 최종 반영
                conn.commit()
                print(f"[VacationControl] 휴가 승인 및 직원({emp_id}) 잔여 휴가 {use_days}일 차감 완료!")
                return True
                
        except Exception as e:
            print(f"[VacationControl] 휴가 승인 처리 중 에러 발생: {e}")
            conn.rollback() # 에러 발생 시 복구
            return False
        finally:
            if conn: conn.close()

    def reject_vacation(self, vac_id, man_id, reason):
        print(f"[VacationControl] 거절 처리 -> 관리자({man_id}), 휴가ID({vac_id})")
        new_status = Vacation.update_status(vac_id, "거절됨", reason)
        return True if new_status == "거절됨" else False
    
    # 다이어그램: 6. check_remain_vacation()
    def check_remain_vacation(self, emp_id, request_days):
        print(f"[VacationControl] check_remain_vacation() 실행 -> ID: {emp_id}, 신청일수: {request_days}일")
        emp_info = Employee.find_by_id(emp_id) #
        
        if emp_info:
            remain = emp_info.get("remain_vacation", 0)
            if remain >= request_days: #
                return True
        return False

    # 다이어그램: 8. request_vacation()
    def request_vacation(self, req_info):
        print(f"[VacationControl] request_vacation() 실행 -> 휴가 DB 저장 요청")
        Vacation.save(req_info) # 다이어그램: 9. save()
        return True
    