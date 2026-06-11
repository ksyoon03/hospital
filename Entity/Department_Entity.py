from DB_Manager import DBManager

# 부서 관련 DB 처리를 담당하는 엔터티
class Department:
    # 부서 ID를 입력받아 해당 부서의 이름을 조회하는 메서드
    @classmethod
    def get_department_info(cls, dep_id):
        conn = DBManager.get_connection() # DB 연결
        try:
            with conn.cursor() as cursor:
                sql = "SELECT dep_name FROM department WHERE dep_id = %s"
                cursor.execute(sql, (dep_id,))
                result = cursor.fetchone()
                # 조회된 결과가 있으면 반환
                # 없으면 기본값 (미배정) 반환
                return result if result else {"dep_name": "미배정"}
        finally:
            conn.close() # DB 연결 해제

    # DB에 등록된 모든 부서의 이름을 리스트 형태로 조회하는 메서드
    @classmethod
    def get_all_department_names(cls):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT dep_name FROM department"
                cursor.execute(sql)
                # 리스트 컴프리헨션을 사용하여 부서명(dep_name)만 추출해 리스트로 반환
                return [row["dep_name"] for row in cursor.fetchall()]
        finally:
            conn.close()

    # 부서명을 입력받아 해당 부서의 ID 조회하는 메서드
    @classmethod
    def get_id_by_name(cls, dep_name):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT dep_id FROM department WHERE dep_name = %s"
                cursor.execute(sql, (dep_name,))
                result = cursor.fetchone()
                # 조회된 결과가 있으면 해당 ID를 반환
                # 없으면 기본값 1 반환
                return result["dep_id"] if result else 1
        finally:
            conn.close()