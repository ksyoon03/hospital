from DB_Manager import DBManager

# 근무일 정보를 관리하는 엔터티
class Schedule:
    # 직원의 근무 스케줄을 추가하는 메서드
    @classmethod
    def insert(cls, sc_info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 같은 직원이 동일한 날짜에 중복 스케줄이 있는지 사전 검사
                cursor.execute("SELECT sc_id FROM schedule WHERE emp_id=%s AND working_day=%s", (sc_info["emp_id"], sc_info["working_day"]))
                if cursor.fetchone():
                    return "DUP" # 중복

                # 중복이 없다면 정상적으로 INSERT 쿼리 실행
                sql = "INSERT INTO schedule (emp_id, man_id, working_day, work_type_id, working_time) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (sc_info["emp_id"], sc_info["man_id"], sc_info["working_day"], sc_info["work_type_id"], sc_info["working_time"]))
                conn.commit()
                return "OK" # 성공 시 OK 반환
        except Exception as e:
            print(f"[Schedule] 스케줄 등록 실패: {e}")
            return "FAIL" # 예외 발생 시 FAIL 반환
        finally:
            if conn: conn.close()

    # 기존 스케줄 정보를 수정하는 메서드
    @classmethod
    def update(cls, sc_info):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                # 스케줄 ID를 조건으로 근무 정보 업데이트
                sql = "UPDATE schedule SET working_day=%s, work_type_id=%s, working_time=%s WHERE sc_id=%s"
                cursor.execute(sql, (sc_info["working_day"], sc_info["work_type_id"], sc_info["working_time"], sc_info["sc_id"]))
                conn.commit()
                return True
        except Exception as e:
            print(f"[Schedule] 스케줄 수정 실패: {e}")
            return False
        finally:
            if conn: conn.close()

    # 특정 스케줄을 DB에서 삭제하는 메서드
    @classmethod
    def delete(cls, sc_id):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM schedule WHERE sc_id = %s", (sc_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"[Schedule] 스케줄 삭제 실패: {e}")
            return False
        finally:
            if conn: conn.close()

    # 특정 직원의 전체 스케줄을 날짜 오름차순으로 조회하는 메서드
    @classmethod
    def find_by_emp(cls, emp_id):
        conn = DBManager.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM schedule WHERE emp_id = %s ORDER BY working_day ASC"
                cursor.execute(sql, (emp_id,))
                return cursor.fetchall()
        except Exception as e:
            return [] # 실패 시 빈 리스트 반환
        finally:
            if conn: conn.close()