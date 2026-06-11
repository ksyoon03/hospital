from DB_Manager import DBManager

# 휴가 신청 및 처리 내역을 관리하는 엔터티
class Vacation:
    # 전체 직원의 휴가 신청 내역을 상세 조회하는 메서드
    @classmethod
    def get_all(cls):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # JOIN을 활용하여 휴가 정보뿐만 아니라 신청한 직원 이름과 부서명도 함께 가져옴
                sql = """
                    SELECT v.*, e.emp_name, d.dep_name 
                    FROM vacation v 
                    JOIN employee e ON v.emp_id = e.emp_id
                    LEFT JOIN department d ON e.dep_id = d.dep_id
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"[Vacation] 휴가 DB 조회 실패: {e}")
            return []
        finally:
            if conn: conn.close()

    # 관리자가 휴가 신청건의 승인/거절 상태와 사유를 업데이트하는 메서드
    @classmethod
    def update_status(cls, vac_id, new_status, reason=""):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE vacation SET vac_status = %s, reason = %s WHERE vac_id = %s"
                cursor.execute(sql, (new_status, reason, vac_id))
                conn.commit()
                return new_status
        finally:
            conn.close()

    # 직원이 신청한 휴가 내역을 DB에 저장하는 메서드
    @classmethod
    def save(cls, req_info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 휴가 신청 시 상태는 기본값으로 저장됨 (대기중)
                sql = """
                    INSERT INTO vacation 
                    (vac_type_id, emp_id, start_day, end_day, reason, vac_status) 
                    VALUES (%s, %s, %s, %s, %s, '대기중')
                """
                # req_info 딕셔너리에서 필요한 데이터를 추출하여 쿼리 실행 파라미터로 매핑
                cursor.execute(sql, (
                    req_info["vac_type_id"],
                    req_info["emp_id"],
                    req_info["start_day"],
                    req_info["end_day"],
                    req_info["reason"]
                ))
                conn.commit() # 변경사항 DB 반영
                print("[Vacation] DB에 신청된 휴가 정보 저장 완료")
                return True  # 쿼리 실행 성공 시 시스템 로직 제어용 True 반환
        except Exception as e:
            print(f"[Vacation] 휴가 저장 실패: {e}")
            return False # 실패 시 False 반환
        finally:
            if conn: conn.close() # 작업 완료 후 DB 연결 해제