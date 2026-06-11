import tkinter as tk
from tkinter import ttk, messagebox
from Control.Salary_Control import *
from Entity.Employee_Entity import *
from Entity.Department_Entity import *

# [관리자용] 직원 급여 계산 및 등록 UI 클래스
class SalaryUI:
    def __init__(self, parent_frame):
        print("[MainUI] 화면 크기에 반응하는 SalaryUI 화면으로 전환됩니다.")
        self.parent_frame = parent_frame
        self.control = SalaryControl() # 급여 정산 로직을 처리하는 컨트롤러 연결
        self.target_month = "2026-05"  # 기준 정산 월 (예시 고정값)
        self.selected_emp = None       # 현재 선택된 직원 정보 저장 변수
        self.draw_ui()

    # 급여 관리 화면을 그리는 메서드
    def draw_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        tk.Label(self.parent_frame, text="급여 등록/수정", font=("Arial", 18, "bold"), bg="#f4f6f9").pack(anchor="w", padx=20, pady=(20, 10))

        main_container = tk.Frame(self.parent_frame, bg="#f4f6f9")
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        left_panel = tk.Frame(main_container, bg="white", width=350, relief="solid", bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 15))
        left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(main_container, bg="white", relief="solid", bd=1)
        self.right_panel.pack(side="left", fill="both", expand=True)

        tk.Label(left_panel, text="직원 급여 목록", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=15, pady=15)
        
        search_frame = tk.Frame(left_panel, bg="white")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.entry_search = tk.Entry(search_frame, font=("Arial", 10), relief="solid", bd=1)
        self.entry_search.pack(side="left", fill="x", expand=True, ipady=4)
        self.entry_search.insert(0, "직원명 또는 부서 입력")
        self.entry_search.config(fg="gray")
        
        self.entry_search.bind("<FocusIn>", lambda e: (self.entry_search.delete(0, tk.END), self.entry_search.config(fg="black")) if self.entry_search.get() == "직원명 또는 부서 입력" else None)
        self.entry_search.bind("<FocusOut>", lambda e: (self.entry_search.insert(0, "직원명 또는 부서 입력"), self.entry_search.config(fg="gray")) if not self.entry_search.get() else None)
        
        tk.Button(search_frame, text="조회", bg="#007bff", fg="white", font=("Arial", 10, "bold"), relief="flat").pack(side="left", padx=(5, 0), ipady=3)

        tk.Frame(left_panel, bg="#e9ecef", height=1).pack(fill="x")

        self.list_canvas = tk.Canvas(left_panel, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.list_canvas.yview)
        self.scroll_frame = tk.Frame(self.list_canvas, bg="white")

        self.scroll_frame.bind("<Configure>", lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all")))
        self.list_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=330)
        
        self.list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.list_canvas.configure(yscrollcommand=scrollbar.set)

        self.load_employee_list() # DB에서 목록 불러오기
        self.show_empty_detail()

    # DB에서 직원 목록 및 급여 등록 상태를 출력하는 메서드
    def load_employee_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        employees = Employee.get_all_employees()
        for emp in employees:            
            dept_info = Department.get_department_info(emp["dep_id"])
            sal_data = self.control.get_salary_info(emp["emp_id"], self.target_month)
            status_text = "등록완료" if sal_data else "미등록" # 해당 월에 급여 내역이 있는지 확인
            
            card = tk.Frame(self.scroll_frame, bg="white", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
            card.pack(fill="x", pady=5, padx=10)

            def make_click_handler(e_data, d_name, s_data):
                return lambda e: self.show_salary_detail(e_data, d_name, s_data)

            handler = make_click_handler(emp, dept_info["dep_name"], sal_data)
            card.bind("<Button-1>", handler)

            top_frame = tk.Frame(card, bg="white")
            top_frame.pack(fill="x", padx=10, pady=(10, 5))
            tk.Label(top_frame, text=f"{emp['emp_name']} / {dept_info['dep_name']}", font=("Arial", 11, "bold"), bg="white").pack(side="left")
            
            bottom_frame = tk.Frame(card, bg="white")
            bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
            tk.Label(bottom_frame, text=f"{self.target_month[:4]}년 {int(self.target_month[5:])}월 급여", font=("Arial", 9), bg="white", fg="#6c757d").pack(side="left")
            
            bg_color, fg_color = ("#d4edda", "#155724") if status_text == "등록완료" else ("#fff3cd", "#856404")
            lbl_status = tk.Label(bottom_frame, text=status_text, font=("Arial", 9, "bold"), bg=bg_color, fg=fg_color, padx=6, pady=2)
            lbl_status.pack(side="left", padx=(10, 0))

            for child in top_frame.winfo_children() + bottom_frame.winfo_children():
                child.bind("<Button-1>", handler)

    # 아무 직원도 선택하지 않았을 때 우측 패널에 표시되는 기본 화면
    def show_empty_detail(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        tk.Label(self.right_panel, text="상세 정보 및 처리", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=15)
        tk.Frame(self.right_panel, bg="#e9ecef", height=1).pack(fill="x")

    # 특정 직원을 클릭했을 때, 우측 패널에 해당 직원의 급여 정보와 폼을 그려주는 메서드
    def show_salary_detail(self, emp, dep_name, sal_data):
        self.selected_emp = emp
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        print(f"[SalaryUI] show_salary_detail() 렌더링 -> 직원: {emp['emp_name']}")

        tk.Label(self.right_panel, text="상세 정보 및 처리", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=15)
        tk.Frame(self.right_panel, bg="#e9ecef", height=1).pack(fill="x")

        content = tk.Frame(self.right_panel, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=20)

        info_top = tk.Frame(content, bg="white")
        info_top.pack(fill="x", pady=(0, 20))

        # 직원 정보 박스
        box1 = tk.Frame(info_top, bg="white", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
        box1.pack(side="left", fill="both", expand=True, padx=(0, 10), ipady=10)
        tk.Label(box1, text=f"직원명: {emp['emp_name']}", font=("Arial", 10), bg="white").pack(anchor="w", padx=15, pady=2)
        tk.Label(box1, text=f"부서명: {dep_name}", font=("Arial", 10), bg="white").pack(anchor="w", padx=15, pady=2)
        tk.Label(box1, text=f"지급 월: {self.target_month[:4]}년 {int(self.target_month[5:])}월", font=("Arial", 10), bg="white").pack(anchor="w", padx=15, pady=2)

        # 근무 시간 요약 및 상태 박스
        is_registered = bool(sal_data)
        status_text = "등록완료" if is_registered else "미등록"

        box2 = tk.Frame(info_top, bg="white", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
        box2.pack(side="left", fill="both", expand=True, padx=(10, 0), ipady=10)
        
        # DB 데이터 여부에 따라 기본값 초기화
        self.current_calc_days = sal_data.get("work_days", 0) if sal_data else 0
        self.current_calc_hours = sal_data.get("total_hours", 0) if sal_data else 0

        self.lbl_work_days = tk.Label(box2, text=f"근무일수: {self.current_calc_days}일", font=("Arial", 10), bg="white")
        self.lbl_work_days.pack(anchor="w", padx=15, pady=2)
        
        self.lbl_total_hours = tk.Label(box2, text=f"총 근무시간: {self.current_calc_hours}시간", font=("Arial", 10), bg="white")
        self.lbl_total_hours.pack(anchor="w", padx=15, pady=2)
        
        tk.Label(box2, text=f"등록 상태: {status_text}", font=("Arial", 10), bg="white").pack(anchor="w", padx=15, pady=2)

        # 세부 항목 입력 폼
        form_frame = tk.Frame(content, bg="white")
        form_frame.pack(fill="x", pady=(10, 20))

        def create_input(parent, label_text, default_val=0, row=0, col=0):
            frame = tk.Frame(parent, bg="white")
            frame.grid(row=row, column=col, padx=(0, 20) if col==0 else 0, pady=10, sticky="ew")
            parent.grid_columnconfigure(col, weight=1)
            tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
            entry = tk.Entry(frame, font=("Arial", 11), relief="solid", bd=1)
            entry.pack(fill="x", ipady=5)
            entry.insert(0, str(default_val))
            return entry

        b_sal = sal_data["basic_sal"] if sal_data else 0
        w_allow = sal_data["work_allowance"] if sal_data else 0
        n_allow = sal_data["night_allowance"] if sal_data else 0
        deduct = sal_data["deductible"] if sal_data else 0

        self.entry_basic = create_input(form_frame, "기본급", b_sal, 0, 0)
        self.entry_work = create_input(form_frame, "근무수당", w_allow, 0, 1)
        self.entry_night = create_input(form_frame, "야간수당", n_allow, 1, 0)
        self.entry_deduct = create_input(form_frame, "공제액", deduct, 1, 1)

        # 최종 지급액 표시
        total_frame = tk.Frame(content, bg="#eef2fd", relief="flat")
        total_frame.pack(fill="x", pady=20, ipady=15)
        tk.Label(total_frame, text="최종 급여", font=("Arial", 12, "bold"), bg="#eef2fd", fg="#333333").pack(side="left", padx=20)
        
        calc_total = (b_sal + w_allow + n_allow) - deduct
        self.lbl_total = tk.Label(total_frame, text=f"{calc_total:,}원", font=("Arial", 16, "bold"), bg="#eef2fd", fg="#4b49ac")
        self.lbl_total.pack(side="right", padx=20)

        btn_frame = tk.Frame(content, bg="white")
        btn_frame.pack(fill="x", pady=(10, 0))

        tk.Button(btn_frame, text="저장", bg="#28a745", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", width=10, command=self.click_save).pack(side="right", ipady=5)
        tk.Button(btn_frame, text="수정" if is_registered else "초기화", bg="#6f42c1", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", width=10).pack(side="right", padx=10, ipady=5)
        
        # 다이어그램 6: 자동 급여 계산 버튼 
        tk.Button(btn_frame, text="급여 계산", bg="#6c757d", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", width=10, command=self.click_calculate).pack(side="right", ipady=5)

    # 급여 계산 버튼을 눌렀을 때 컨트롤러를 통해 자동 정산을 수행하는 메서드
    def click_calculate(self):
        # 컨트롤러에 시급, 근무일정 기반 계산 요청
        calc_data = self.control.calculate_salary(self.selected_emp["emp_id"], self.target_month)
        
        # 계산된 근무 정보를 화면에 반영
        self.current_calc_days = calc_data["work_days"]
        self.current_calc_hours = calc_data["total_hours"]
        self.lbl_work_days.config(text=f"근무일수: {self.current_calc_days}일")
        self.lbl_total_hours.config(text=f"총 근무시간: {self.current_calc_hours}시간")

        # 계산된 금액을 입력 폼에 덮어쓰기
        self.entry_basic.delete(0, tk.END)
        self.entry_basic.insert(0, str(calc_data["basic_sal"]))
        self.entry_work.delete(0, tk.END)
        self.entry_work.insert(0, str(calc_data["work_allowance"]))
        self.entry_night.delete(0, tk.END)
        self.entry_night.insert(0, str(calc_data["night_allowance"]))
        self.entry_deduct.delete(0, tk.END)
        self.entry_deduct.insert(0, str(calc_data["deductible"]))

        # 최종 지급액 텍스트 변경
        total = (calc_data["basic_sal"] + calc_data["work_allowance"] + calc_data["night_allowance"]) - calc_data["deductible"]
        self.lbl_total.config(text=f"{total:,}원")
        print("[SalaryUI] 급여 계산 및 UI 반영 완료")

    # 저장 버튼 클릭 시 입력된 내용을 바탕으로 DB에 급여 데이터를 저장하는 메서드
    def click_save(self):
        sal_info = {
            "emp_id": self.selected_emp["emp_id"],
            "man_id": "admin",
            "sal_date": self.target_month,
            "basic_sal": int(self.entry_basic.get()),
            "work_allowance": int(self.entry_work.get()),
            "night_allowance": int(self.entry_night.get()),
            "deductible": int(self.entry_deduct.get()),
            "work_days": getattr(self, 'current_calc_days', 0),
            "total_hours": getattr(self, 'current_calc_hours', 0)
        }
        
        print(f"[SalaryUI] click_save() 실행 -> 데이터: {sal_info}")
        success = self.control.register_salary(sal_info)
        
        if success:
            messagebox.showinfo("저장 완료", "급여 정보가 성공적으로 저장되었습니다.")
            self.load_employee_list()
            dep_info = Department.get_department_info(self.selected_emp["dep_id"])
            self.show_salary_detail(self.selected_emp, dep_info["dep_name"], sal_info)


# [일반 직원용] 자신의 급여 명세서를 조회하는 UI 클래스
class EmpSalaryUI:
    def __init__(self, parent_frame, user_id):
        print(f"[MainUI] 일반 직원({user_id}) 급여 조회 화면으로 전환됩니다.")
        self.parent_frame = parent_frame
        self.user_id = user_id
        self.control = SalaryControl()

        # 현재 직원의 기본 정보 로드
        emp_info = Employee.find_by_id(self.user_id)
        if emp_info:
            self.emp_name = emp_info["emp_name"]
            dep_info = Department.get_department_info(emp_info["dep_id"])
            self.dep_name = dep_info["dep_name"]
        else:
            self.emp_name = "알 수 없음"
            self.dep_name = "알 수 없음"

        self.draw_ui()

    # 급여 조회 화면 구성 메서드
    def draw_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        bg_frame = tk.Frame(self.parent_frame, bg="#f4f6f9")
        bg_frame.pack(fill="both", expand=True)

        outer_container = tk.Frame(bg_frame, bg="white", relief="flat")
        outer_container.pack(fill="both", expand=True, padx=30, pady=30)

        # 화면이 작을 경우를 대비해 스크롤 설정
        self.canvas = tk.Canvas(outer_container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(outer_container, orient="vertical", command=self.canvas.yview)
        main_container = tk.Frame(self.canvas, bg="white")

        main_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=main_container, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        tk.Label(main_container, text="급여 조회", font=("Arial", 20, "bold"), bg="white", fg="#212529").pack(anchor="w", pady=(10, 25))

        info_frame = tk.Frame(main_container, bg="white")
        info_frame.pack(fill="x", pady=(0, 25))

        box1 = tk.Frame(info_frame, bg="#f8f9fa", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
        box1.pack(side="left", fill="both", expand=True, padx=(0, 10), ipady=15)
        tk.Label(box1, text=f"직원명:  {self.emp_name}", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#212529").pack(anchor="w", padx=20, pady=(5, 5))
        tk.Label(box1, text=f"소속 부서:  {self.dep_name}", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#212529").pack(anchor="w", padx=20)

        box2 = tk.Frame(info_frame, bg="#f8f9fa", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
        box2.pack(side="left", fill="both", expand=True, padx=(10, 0), ipady=15)
        tk.Label(box2, text="조회 가능 항목:", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#212529").pack(anchor="w", padx=20, pady=(5, 5))
        tk.Label(box2, text="근무일수, 총 근무시간, 기본급, 근무수당, 야간수당, 공제액, 최종 급여", font=("Arial", 10), bg="#f8f9fa", fg="#495057").pack(anchor="w", padx=20)

        tk.Label(main_container, text="지급 월 선택", font=("Arial", 11, "bold"), bg="white", fg="#212529").pack(anchor="w", pady=(10, 5))
        search_frame = tk.Frame(main_container, bg="white")
        search_frame.pack(fill="x", pady=(0, 20))

        # 콤보박스로 조회 월 선택
        months = [f"2026년 {i}월" for i in range(1, 13)]
        self.combo_month = ttk.Combobox(search_frame, values=months, state="readonly", font=("Arial", 12))
        self.combo_month.set("2026년 5월") 
        self.combo_month.pack(side="left", fill="x", expand=True, ipady=6)

        tk.Button(search_frame, text="조회", bg="#6366f1", fg="white", font=("Arial", 11, "bold"), relief="flat", width=8, cursor="hand2", command=self.click_search).pack(side="left", padx=(10, 0), ipady=5)

        self.table_frame = tk.Frame(main_container, bg="white", relief="solid", bd=0)
        self.table_frame.pack(fill="x", pady=(10, 20)) 

        self.render_empty_table()

    # 조회 전 초기 화면 메시지 렌더링
    def render_empty_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        tk.Frame(self.table_frame, bg="#dee2e6", height=1).pack(fill="x")
        tk.Label(self.table_frame, text="조회 버튼을 눌러 급여 내역을 확인해주세요.", font=("Arial", 11), bg="white", fg="#adb5bd").pack(pady=50)
        tk.Frame(self.table_frame, bg="#dee2e6", height=1).pack(fill="x")

    # 조회 버튼 클릭 시 호출
    def click_search(self):
        selected = self.combo_month.get()
        year = selected.split("년")[0].strip()
        month = selected.split("년")[1].replace("월", "").strip()
        target_month = f"{year}-{int(month):02d}"

        print(f"🖱️ [EmpSalaryUI] 급여 조회 클릭 -> 대상 월: {target_month}")
        sal_data = self.control.get_salary_info(self.user_id, target_month)
        self.show_salary_detail(sal_data)

    # 검색된 급여 데이터를 표 형태로 렌더링하는 메서드
    def show_salary_detail(self, sal_data):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # 데이터가 없을 때 처리
        if not sal_data:
            tk.Frame(self.table_frame, bg="#dee2e6", height=1).pack(fill="x")
            tk.Label(self.table_frame, text="해당 월의 급여 내역이 존재하지 않습니다.", font=("Arial", 12, "bold"), bg="white", fg="#e64980").pack(pady=50)
            tk.Frame(self.table_frame, bg="#dee2e6", height=1).pack(fill="x")
            return
        
        # 테이블의 한 줄을 깔끔하게 추가하는 공통 유틸리티
        def add_row(parent, label_text, value_text, is_last=False):
            row = tk.Frame(parent, bg="white")
            row.pack(fill="x")

            lbl_bg = "#f4f6f9" if not is_last else "#eef2fd"
            lbl_fg = "#495057" if not is_last else "#4b49ac"
            lbl_font = ("Arial", 11, "bold") if not is_last else ("Arial", 12, "bold")

            left_cell = tk.Label(row, text=label_text, font=lbl_font, bg=lbl_bg, fg=lbl_fg, width=18, anchor="w", padx=20)
            left_cell.pack(side="left", fill="y", ipady=12)

            val_bg = "white" if not is_last else "#eef2fd"
            val_fg = "black" if not is_last else "#4b49ac"
            val_font = ("Arial", 11, "bold") if not is_last else ("Arial", 14, "bold")

            right_cell = tk.Label(row, text=value_text, font=val_font, bg=val_bg, fg=val_fg, anchor="e", padx=20)
            right_cell.pack(side="left", fill="both", expand=True, ipady=12)

            if not is_last:
                tk.Frame(parent, bg="#e9ecef", height=1).pack(fill="x")

        tk.Frame(self.table_frame, bg="#dee2e6", height=1).pack(fill="x")

        # 각 항목별 데이터 삽입 및 테이블 줄 생성
        work_days = f"{sal_data.get('work_days', 0)}일"
        total_hours = f"{sal_data.get('total_hours', 0)}시간"

        add_row(self.table_frame, "근무일수", work_days)
        add_row(self.table_frame, "총 근무시간", total_hours)
        add_row(self.table_frame, "기본급", f"{sal_data['basic_sal']:,}원")
        add_row(self.table_frame, "근무수당", f"{sal_data['work_allowance']:,}원")
        add_row(self.table_frame, "야간수당", f"{sal_data['night_allowance']:,}원")
        add_row(self.table_frame, "공제액", f"{sal_data['deductible']:,}원")

        # 최종 급여 출력
        total = (sal_data['basic_sal'] + sal_data['work_allowance'] + sal_data['night_allowance']) - sal_data['deductible']
        add_row(self.table_frame, "최종 급여", f"{total:,}원", is_last=True)