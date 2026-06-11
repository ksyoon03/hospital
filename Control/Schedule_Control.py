import datetime
from DB_Manager import DBManager
from Entity.Department_Entity import Department
from Entity.Employee_Entity import Employee
from Entity.Schedule_Entity import Schedule
from Entity.WorkType_Entity import WorkType

# 직원 근무일을 관리하는 컨트롤러
class ScheduleControl:
    # 근무일 등록을 위해 이름으로 직원을 필터링하여 가져오는 메서드
    def get_all_employees_for_schedule(self, search_kw=""):
        employees = Employee.get_all_employees()
        result = []
        for emp in employees:
            # 검색어가 있고, 직원 이름에 검색어가 포함되지 않으면 건너뜀
            if search_kw and search_kw not in emp["emp_name"]:
                continue
            dept_info = Department.get_department_info(emp["dep_id"])
            result.append({
                "emp_id": emp["emp_id"],
                "emp_name": emp["emp_name"],
                "dep_name": dept_info["dep_name"]
            })
        return result

    # 특정 직원의 전체 근무일을 조회하는 메서드
    def get_emp_schedules(self, emp_id):
        schedules = Schedule.find_by_emp(emp_id)
        res = []
        for sc in schedules:
            res.append({
                "sc_id": sc["sc_id"],
                "working_day": sc["working_day"],
                "work_type_name": WorkType.get_type_name(sc["work_type_id"]), # DB ID를 근무 명칭으로 변환
                "working_time": sc["working_time"]
            })
        return res

    # 관리자가 직원의 새로운 근무일 등록하는 메서드
    def register_schedule(self, sc_info):
        # 1. 근무 명칭을 DB 저장을 위한 근무 타입 ID로 변환
        sc_info["work_type_id"] = WorkType.get_type_id(sc_info["work_type_name"])
        sc_info["man_id"] = "admin" # 등록 주체(관리자) 고정
        
        # 2. 근무 시간에 따라 일괄적으로 8시간 할당 로직 적용, 휴무는 0시간 적용
        sc_info["working_time"] = 8 if sc_info["work_type_name"] != "휴무" else 0
        
        return Schedule.insert(sc_info)

    # 기존 근무일을 수정하는 메서드
    def modify_schedule(self, sc_info):
        sc_info["work_type_id"] = WorkType.get_type_id(sc_info["work_type_name"])
        sc_info["working_time"] = 8 if sc_info["work_type_name"] != "휴무" else 0
        return Schedule.update(sc_info)

    # 등록된 근무일을 삭제하는 메서드
    def remove_schedule(self, sc_id):
        return Schedule.delete(sc_id)

    # 직원이 자신의 한 달 치 근무 일정 및 휴가를 통합하여 캘린더용으로 조회하는 메서드
    def get_my_schedule(self, emp_id, year, month):
        print(f"[ScheduleControl] get_my_schedule() 호출 -> ID: {emp_id}, 조회월: {year}년 {month}월")
        sched_dict = {} # 날짜(일)를 Key로, 근무상태를 Value로 저장할 딕셔너리
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 일반 근무 근무일 조회 및 딕셔너리 매핑
                sql_schedule = "SELECT working_day, work_type_id FROM schedule WHERE emp_id = %s AND YEAR(working_day) = %s AND MONTH(working_day) = %s"
                cursor.execute(sql_schedule, (emp_id, year, month))
                schedules = cursor.fetchall()
                
                for sch in schedules:
                    w_day = sch["working_day"]
                    day_num = w_day.day if hasattr(w_day, 'day') else int(str(w_day).split("-")[2])
                    sched_dict[day_num] = WorkType.get_type_name(sch["work_type_id"])

                # 2. 승인된 휴가 내역 조회
                sql_vacation = """
                    SELECT start_day, end_day FROM vacation WHERE emp_id = %s AND vac_status = '승인됨'
                      AND ((YEAR(start_day) = %s AND MONTH(start_day) = %s) OR (YEAR(end_day) = %s AND MONTH(end_day) = %s) OR (start_day <= LAST_DAY(STR_TO_DATE(%s, '%%Y-%%m-%%d')) AND end_day >= STR_TO_DATE(%s, '%%Y-%%m-%%d')))
                """
                target_date_str = f"{year}-{month:02d}-01"
                cursor.execute(sql_vacation, (emp_id, year, month, year, month, target_date_str, target_date_str))
                vacations = cursor.fetchall()
                
                # 3. 휴가 기간을 순회하며 해당되는 날짜를 휴가로 덮어쓰기
                import calendar as cal_mod
                _, last_day = cal_mod.monthrange(year, month)
                
                for vac in vacations:
                    s_day = vac["start_day"]
                    e_day = vac["end_day"]
                    # 문자열인 경우 datetime 객체로 변환
                    s_date = s_day if hasattr(s_day, 'year') else datetime.datetime.strptime(str(s_day), '%Y-%m-%d').date()
                    e_date = e_day if hasattr(e_day, 'year') else datetime.datetime.strptime(str(e_day), '%Y-%m-%d').date()
                    
                    # 1일부터 말일까지 확인하여 휴가 기간에 속하면 휴가 등록
                    for d in range(1, last_day + 1):
                        current_date = datetime.date(year, month, d)
                        if s_date <= current_date <= e_date:
                            sched_dict[d] = "휴가" 
        except Exception as e:
            print(f"[ScheduleControl] 개인 근무일정 및 휴가 연동 오류: {e}")
        finally:
            if conn: conn.close()
            
        return sched_dict # 최종 완성된 근무일 딕셔너리 반환