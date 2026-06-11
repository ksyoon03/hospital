from DB_Manager import DBManager
from Entity.Employee_Entity import Employee
from Entity.Manager_Entity import Manager
from Entity.Department_Entity import Department

# 로그인 및 회원가입을 담당하는 컨트롤러
class AuthControl:
    # 로그인을 처리하는 메서드
    def authenticate(self, user_id, user_pw):
        print(f"[AuthControl] 로그인 시도 -> ID: {user_id}")
        conn = DBManager.get_connection()
        if not conn: 
            return False

        try:
            with conn.cursor() as cursor:
                # 1. 관리자 테이블에서 계정 존재 여부 및 비밀번호 일치 확인
                sql_man = "SELECT * FROM manager WHERE man_id = %s AND man_pw = %s"
                cursor.execute(sql_man, (user_id, user_pw))
                if cursor.fetchone():
                    print("[AuthControl] 관리자 계정 인증 성공")
                    return True

                # 2. 관리자가 아니라면 일반 직원 테이블에서 확인
                sql_emp = "SELECT * FROM employee WHERE emp_id = %s AND emp_pw = %s"
                cursor.execute(sql_emp, (user_id, user_pw))
                if cursor.fetchone():
                    print("[AuthControl] 일반 직원 계정 인증 성공")
                    return True
                    
        except Exception as e:
            print(f"[AuthControl] 로그인 DB 조회 에러: {e}")
        finally:
            conn.close()
            
        print("[AuthControl] 인증 실패 (아이디 또는 비밀번호 불일치)")
        return False

    # 사용자가 관리자인지 일반 직원인지 권한을 확인하는 메서드
    def check_permission(self, user_id):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 관리자 테이블에 해당 ID가 존재하면 Manager 권한 부여
                sql_man = "SELECT man_id FROM manager WHERE man_id = %s"
                cursor.execute(sql_man, (user_id,))
                if cursor.fetchone():
                    return "Manager"
                
                # 존재하지 않으면 기본적으로 Employee 권한 부여
                return "Employee"
        except Exception as e:
            print(f"[AuthControl] 권한 DB 조회 에러: {e}")
            return "Employee"
        finally:
            if conn:
                conn.close()

    # 회원가입 시 아이디 중복을 검사하는 메서드
    def check_duplicate(self, user_id):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 관리자 테이블에서 중복 확인
                cursor.execute("SELECT man_id FROM manager WHERE man_id=%s", (user_id,))
                if cursor.fetchone(): return True
                
                # 직원 테이블에서 중복 확인
                cursor.execute("SELECT emp_id FROM employee WHERE emp_id=%s", (user_id,))
                if cursor.fetchone(): return True
        finally:
            if conn: conn.close()
        return False # 중복이 없으면 False 반환

    # 새로운 사용자를 등록(회원가입)하는 메서드
    def reg_user(self, info):
        # 1. 중복 아이디 검사
        if self.check_duplicate(info['id']):
            return "DUP"
        
        # 2. 부서명을 DB 저장을 위한 부서 ID로 변환
        info['dep_id'] = Department.get_id_by_name(info['dep'])
        
        # 3. 관리자 계정 여부에 따라 알맞은 엔터티의 저장 메서드 호출
        if info['is_admin']:
            success = Manager.add_man(info)
        else:
            success = Employee.add_emp(info)
        
        # 성공 여부에 따라 상태 코드 반환
        return "OK" if success else "FAIL"