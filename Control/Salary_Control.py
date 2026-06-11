from DB_Manager import DBManager
from Entity.Salary_Entity import Salary

# 직원 급여 관리를 담당하는 컨트롤러
class SalaryControl:
    # 특정 직원의 특정 월에 대한 최종 급여를 계산하는 메서드
    def calculate_salary(self, emp_id, target_month):
        print(f"[SalaryControl] calculate_salary() 실행 -> {emp_id}의 {target_month} 실제 급여 계산")
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 직원 개인의 시급 조회 (DB에 값이 없으면 기본 12,000원으로 설정)
                cursor.execute("SELECT hourly_wage FROM employee WHERE emp_id = %s", (emp_id,))
                emp_row = cursor.fetchone()
                hourly_wage = emp_row["hourly_wage"] if emp_row and "hourly_wage" in emp_row else 12000

                # 2. 해당 월의 실제 근무일 데이터 조회
                year, month = target_month.split("-")
                sql = """
                    SELECT work_type_id, working_time
                    FROM schedule
                    WHERE emp_id = %s AND YEAR(working_day) = %s AND MONTH(working_day) = %s
                """
                cursor.execute(sql, (emp_id, year, month))
                schedules = cursor.fetchall()

                work_days, total_hours, night_hours = 0, 0, 0

                # 3. 근무일을 순회하며 총 근무일수, 근무시간, 야간근무시간 계산
                for sch in schedules:
                    w_type = sch["work_type_id"]
                    w_time = sch["working_time"] if sch["working_time"] else 0

                    if w_type != 4: # 휴무가 아닌 경우에만 출근으로 인정
                        work_days += 1
                        total_hours += w_time
                        if w_type == 3: # 야간인 경우 야간 수당을 위해 별도 시간 누적
                            night_hours += w_time

                # 4. 최종 급여 수식 적용 및 정산
                basic_sal = total_hours * hourly_wage # 기본급 (총 시간 * 시급)
                work_allowance = work_days * 15000    # 출근 수당 (1일당 식대/교통비 1.5만원)
                night_allowance = night_hours * int(hourly_wage * 0.5) # 야간 할증 (시급의 50% 추가)
                deductible = int((basic_sal + work_allowance + night_allowance) * 0.1) # 4대보험 등 10% 일괄 공제

                # 계산된 상세 내역 반환
                return {
                    "work_days": work_days,
                    "total_hours": total_hours,
                    "basic_sal": basic_sal,
                    "work_allowance": work_allowance,
                    "night_allowance": night_allowance,
                    "deductible": deductible
                }
        except Exception as e:
            print(f"[SalaryControl] 급여 계산 중 에러: {e}")
            return {"work_days": 0, "total_hours": 0, "basic_sal": 0, "work_allowance": 0, "night_allowance": 0, "deductible": 0}
        finally:
            if conn: conn.close()

    # 계산 완료된 급여 데이터를 DB에 저장하도록 엔터티에 요청하는 메서드
    def register_salary(self, sal_info):
        print(f"[SalaryControl] register_salary() 실행 -> 급여 데이터 검증 및 저장 요청")
        Salary.save(sal_info)
        return True

    # 특정 직원의 특정 월 급여 명세서를 DB에서 가져오는 메서드
    def get_salary_info(self, emp_id, target_month):
        return Salary.find_by_month(emp_id, target_month)