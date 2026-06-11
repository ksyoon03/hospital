from DB_Manager import DBManager

# 병원의 근무 종류와 근무 시간을 관리하고 매핑하는 엔터티
class WorkType:
    # DB에 저장되는 근무 ID와 근무 유형명을 매핑한 딕셔너리
    TYPES = {1: "주간", 2: "오후", 3: "야간", 4: "휴무"}
    
    # 근무 유형명에 따른 병원의 고정 근무 시간표 (상수)
    TIMES = {
        "주간": "07:00 ~ 15:00",
        "오후": "15:00 ~ 23:00",
        "야간": "23:00 ~ 07:00",
        "휴무": "00:00 ~ 00:00"
    }

    # DB에 저장된 근무 유형 ID를 UI나 화면에 출력할 문자로 반환하는 메서드
    @classmethod
    def get_type_name(cls, type_id):
        # 매핑된 값이 없을 경우 기본값으로 "미정"을 반환
        return cls.TYPES.get(type_id, "미정")

    # 화면에서 전달받은 문자열을 DB 저장을 위한 정수형 ID로 역변환하는 메서드
    @classmethod
    def get_type_id(cls, type_name):
        for t_id, t_name in cls.TYPES.items():
            if t_name == type_name:
                return t_id # 일치하는 값이 있으면 해당 ID 값으로 반환
        return 1 # 일치하는 값이 없으면 기본 ID 1 (주간) 반환

    # 해당 근무 종류명에 맞는 실제 근무 시간을 반환하는 메서드
    @classmethod
    def get_time(cls, type_name):
        return cls.TIMES.get(type_name, "00:00 ~ 00:00")