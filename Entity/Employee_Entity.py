from DB_Manager import DBManager

# 일반 직원 DB 관리를 담당하는 엔터티
class Employee:
    # 직원 ID를 기준으로 특정 직원의 상세 정보를 조회하는 메서드
    @classmethod
    def find_by_id(cls, emp_id):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM employee WHERE emp_id = %s"
                cursor.execute(sql, (emp_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    # DB에 등록된 모든 일반 직원의 정보를 조회하는 메서드
    @classmethod
    def get_all_employees(cls):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 관리자를 제외한 일반 직원 목록만 조회
                sql = "SELECT * FROM employee"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()

    # 기존 직원의 부서 정보 및 재직 상태를 업데이트하는 메서드
    @classmethod
    def update(cls, emp_id, info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 딕셔너리 형태의 info 객체에서 데이터를 추출해 DB 업데이트 실행
                sql = "UPDATE employee SET dep_id = %s, emp_status = %s WHERE emp_id = %s"
                cursor.execute(sql, (info["dep_id"], info["emp_status"], emp_id))
                conn.commit() # 변경사항 DB 반영
                print(f"[Employee] DB 업데이트 완료 ID: {emp_id}")
        finally:
            conn.close()

    # 신규 직원을 DB에 INSERT하는 메서드
    @classmethod
    def add_emp(cls, info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 신규 직원은 기본적으로 '재직중' 상태
                # 연차 15일 부여
                sql = "INSERT INTO employee (emp_id, emp_pw, emp_name, dep_id, emp_status, remain_vacation) VALUES (%s, %s, %s, %s, '재직중', 15)"
                cursor.execute(sql, (info['id'], info['pw'], info['name'], info['dep_id']))
                conn.commit()
                return True # 성공 시 True 반환
        except Exception as e:
            print(f"[Employee] DB 저장 에러: {e}")
            return False # 실패 시 False 반환
        finally:
            if conn: conn.close()