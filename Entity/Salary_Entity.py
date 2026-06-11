from DB_Manager import DBManager

# 직원 급여 데이터 관리를 담당하는 엔터티
class Salary:
    # 직원의 해당 월 급여 정보를 DB에 저장하거나 업데이트하는 메서드
    @classmethod
    def save(cls, sal_info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 해당 직원의 해당 월 급여 내역이 있는지 확인
                sql_chk = "SELECT sal_id FROM salary WHERE emp_id = %s AND sal_date = %s"
                cursor.execute(sql_chk, (sal_info["emp_id"], sal_info["sal_date"]))
                exist = cursor.fetchone()

                if exist:
                    # 2. 이미 내역이 있다면 UPDATE 문을 통해 갱신 처리
                    sql_up = "UPDATE salary SET basic_sal=%s, work_allowance=%s, night_allowance=%s, deductible=%s, work_days=%s, total_hours=%s WHERE sal_id=%s"
                    cursor.execute(sql_up, (sal_info["basic_sal"], sal_info["work_allowance"], sal_info["night_allowance"], sal_info["deductible"], sal_info["work_days"], sal_info["total_hours"], exist["sal_id"]))
                else:
                    # 3. 내역이 없다면 INSERT 문을 통해 새로운 급여 정보 등록
                    sql_in = "INSERT INTO salary (emp_id, man_id, sal_date, basic_sal, work_allowance, night_allowance, deductible, work_days, total_hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql_in, (sal_info["emp_id"], sal_info["man_id"], sal_info["sal_date"], sal_info["basic_sal"], sal_info["work_allowance"], sal_info["night_allowance"], sal_info["deductible"], sal_info["work_days"], sal_info["total_hours"]))
                conn.commit()
        finally:
            conn.close()

    # 특정 직원의 특정 월 급여 상세 내역을 조회하는 메서드
    @classmethod
    def find_by_month(cls, emp_id, target_month):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM salary WHERE emp_id = %s AND sal_date = %s"
                cursor.execute(sql, (emp_id, target_month))
                return cursor.fetchone()
        finally:
            conn.close()