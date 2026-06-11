from tkcalendar import DateEntry

# 여러 UI 화면에서 공통으로 사용되는 커스텀 달력 위젯 클래스
class CustomDateEntry(DateEntry):
    # 달력 위젯 클릭 후 포커스를 잃었을 때 발생할 수 있는 기본 에러/오작동을 방지하기 위해
    # 기본 이벤트를 무시하도록 오버라이딩한 메서드
    def _focus_out(self, event):
        pass