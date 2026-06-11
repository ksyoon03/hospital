import tkinter as tk
from Boundary.Schedule_Boundary import ScheduleUI, EmpSchUI
from Boundary.Vacation_Boundary import VacationUI, EmpVacationUI
from Boundary.Salary_Boundary import SalaryUI, EmpSalaryUI
from Boundary.Employee_Boundary import EmployeeManagementUI

# 메인 대시보드 창 클래스
class MainUI:
    def __init__(self, root, role="Employee", user_id=""): 
        self.root = root
        self.role = role         # 접속한 사용자의 권한
        self.user_id = user_id   # 접속한 사용자의 고유 ID
        self.display_dashboard()

    # 메인 대시보드의 레이아웃을 구성하는 메서드
    def display_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        container = tk.Frame(self.root, bg="#f4f6f9")
        container.pack(fill="both", expand=True)

        sidebar = tk.Frame(container, bg="white", width=200, relief="flat", bd=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="메뉴", font=("Arial", 16, "bold"), bg="white", anchor="w").pack(fill="x", padx=30, pady=(40, 30))

        def create_menu_btn(text, fg_color="black", command=None):
            btn = tk.Button(sidebar, text=text, font=("Arial", 11), bg="white", fg=fg_color,
                            relief="flat", anchor="w", cursor="hand2", command=command, activebackground="#f4f6f9")
            btn.pack(fill="x", padx=30, pady=15)
            return btn

        self.content_frame = tk.Frame(container, bg="#f4f6f9")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # 사용자 권한에 따른 메뉴 버튼 생성
        if self.role == "Manager":
            # 관리자용 메뉴 목록
            create_menu_btn("근무일 관리", command=self.navigate_to_schedule)
            create_menu_btn("휴가 관리", command=self.navigate_to_vacation)
            create_menu_btn("급여 관리", command=self.navigate_to_salary)
            create_menu_btn("직원 명부", command=self.navigate_to_employee_mgmt)
        else:
            # 일반 직원용 메뉴 목록
            create_menu_btn("근무일 조회", command=self.navigate_to_emp_sch)
            create_menu_btn("휴가 신청", command=self.navigate_to_emp_vacation) 
            create_menu_btn("급여 조회", command=self.navigate_to_emp_salary)

        logout_frame = tk.Frame(sidebar, bg="white")
        logout_frame.pack(side="bottom", fill="x", pady=40)
        btn_logout = tk.Button(logout_frame, text="로그아웃", font=("Arial", 11), bg="white", fg="red", relief="flat", cursor="hand2", command=self.click_logout)
        btn_logout.pack(fill="x", padx=30)

    # == 이하 화면 전환 메서드 ==

    # 관리자용 - 근무일 관리 화면 호출
    def navigate_to_schedule(self):
        ScheduleUI(self.content_frame)

    # 관리자용 - 직원 명부 화면 호출
    def navigate_to_employee_mgmt(self):
        EmployeeManagementUI(self.content_frame)

    # 관리자용 - 휴가 승인/관리 화면 호출
    def navigate_to_vacation(self):
        VacationUI(self.content_frame)

    # 관리자용 - 급여 계산 및 등록 화면 호출
    def navigate_to_salary(self):
        SalaryUI(self.content_frame)
        
    # 직원용 - 내 근무일/달력 조회 화면 호출
    def navigate_to_emp_sch(self):
        EmpSchUI(self.content_frame, self.user_id)

    # 직원용 - 내 급여 명세서 화면 호출
    def navigate_to_emp_salary(self):
        EmpSalaryUI(self.content_frame, self.user_id)

    # 직원용 - 휴가 신청서 화면 호출
    def navigate_to_emp_vacation(self):
        EmpVacationUI(self.content_frame, self.user_id)

    # 로그아웃 처리 및 로그인 화면으로 복귀하는 메서드
    def click_logout(self):
        from Boundary.Auth_Boundary import LoginUI
        LoginUI(self.root)