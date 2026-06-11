import pymysql

# DB 연결 관리를 담당하는 클래스
class DBManager:
    HOST = '127.0.0.1' # 로컬호스트 주소
    USER = 'root'      # DB 사용자명
    
    PASSWORD = '비밀번호'   # DB 비밀번호
    DB_NAME = 'hospital_db'  # DB 이름

    # 엔터티에서 공통으로 호출하여 DB 커넥션을 가져오는 클래스 메서드
    @classmethod
    def get_connection(cls):
        try:
            # pymysql 라이브러리를 사용하여 MySQL DB와 연결 객체
            conn = pymysql.connect(
                host=cls.HOST,
                user=cls.USER,
                password=cls.PASSWORD,
                database=cls.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor 
            )
            return conn # 연결 성공 시 커넥션 객체 반환
        except Exception as e:
            # DB 연결 실패 시 시스템이 다운되지 않도록 예외 처리 후 에러 로그 출력
            print(f"[DBMangaer] DB 연결 실패: {e}")
            return None