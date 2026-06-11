from DB_Manager import DBManager

# 관리자 데이터를 처리하는 엔터티
class Manager:
    # 신규 관리자 계정을 DB에 INSERT하는 메서드
    @classmethod
    def add_man(cls, info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 신규 관리자는 기본적으로 '재직중' 상태로 저장
                sql = "INSERT INTO manager (man_id, man_pw, man_name, man_status) VALUES (%s, %s, %s, '재직중')"
                cursor.execute(sql, (info['id'], info['pw'], info['name']))
                conn.commit()
                return True # 추가 성공 시 True 반환
        except Exception as e:
            print(f"[Manager] DB 저장 에러: {e}")
            return False # 추가 실패 시 예외 메시지 출력 후 False 반환
        finally:
            if conn: conn.close()