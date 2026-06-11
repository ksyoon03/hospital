import datetime
import calendar
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Boundary.Schedule_Boundary import *
from Boundary.Salary_Boundary import *
from Control.Schedule_Control import *

class CustomDateEntry(DateEntry):
    def _focus_out(self, event):
        pass

# [관리자용] 직원의 근무 근무일을 배정, 수정, 삭제하는 UI 클래스
class ScheduleUI:
    def __init__(self, parent_frame):
        print("[MainUI] 화면 크기에 반응하는 ScheduleUI 화면으로 전환됩니다.")
        self.parent_frame = parent_frame
        self.control = ScheduleControl() # 일정 관리용 컨트롤러
        self.draw_ui()

    def draw_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        tk.Label(self.parent_frame, text="근무일 관리", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#212529").pack(anchor="w", padx=20, pady=(20, 10))

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[15, 5])

        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 근무일 신규 등록
        self.tab_reg = tk.Frame(self.notebook, bg="white")
        # 기존 근무일 열람 및 수정/삭제
        self.tab_mod = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_reg, text="[ScheduleUI] 근무일 등록  ")
        self.notebook.add(self.tab_mod, text="[ScheduleUI] 근무일 수정/삭제  ")

        self.render_register_tab()
        self.render_modify_tab()

    # 근무일 등록 화면 렌더링
    def render_register_tab(self):
        tk.Label(self.tab_reg, text="직원 목록 (근무일 등록)", font=("Arial", 13, "bold"), bg="white").pack(anchor="w", padx=20, pady=15)
        tk.Frame(self.tab_reg, bg="#dee2e6", height=2).pack(fill="x", padx=20)

        # 직원이 많을 수 있으므로 스크롤 리스트로 구성
        list_canvas = tk.Canvas(self.tab_reg, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_reg, orient="vertical", command=list_canvas.yview)
        scroll_frame = tk.Frame(list_canvas, bg="white")
        
        scroll_frame.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        list_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        list_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        list_canvas.configure(yscrollcommand=scrollbar.set)

        # 컨트롤러에서 직원 목록을 받아와서 각 행을 그림
        emp_list = self.control.get_all_employees_for_schedule()
        for emp in emp_list:
            row = tk.Frame(scroll_frame, bg="white")
            row.pack(fill="x", pady=5)

            tk.Label(row, text=emp["emp_name"], font=("Arial", 11, "bold"), bg="white", width=12, anchor="w").pack(side="left", padx=(10, 5))
            tk.Label(row, text=emp["dep_name"], font=("Arial", 11), bg="white", fg="gray", width=15, anchor="w").pack(side="left")
            
            # 근무일 등록 버튼 클릭 시 해당 직원의 정보와 함께 팝업창 오픈
            tk.Button(row, text="근무일 등록", bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", 
                      command=lambda e=emp: self.open_register_popup(e)).pack(side="right", padx=10, ipady=3, ipadx=10)
            
            tk.Frame(scroll_frame, bg="#f1f3f5", height=1).pack(fill="x", pady=5)

    # 신규 근무일 배정 팝업창
    def open_register_popup(self, emp):
        pop = tk.Toplevel(self.parent_frame.winfo_toplevel())
        pop.title(f"근무일 등록 - {emp['emp_name']}")
        pop.geometry("300x350")
        pop.configure(bg="white")
        pop.attributes("-topmost", True)

        tk.Label(pop, text=f"{emp['emp_name']} 근무일 추가", font=("Arial", 14, "bold"), bg="white").pack(pady=20)

        # 날짜 선택
        tk.Label(pop, text="날짜 선택", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=30)
        cal = CustomDateEntry(pop, width=12, date_pattern='yyyy-mm-dd', font=("Arial", 11))
        cal.pack(fill="x", padx=30, pady=(5, 15), ipady=3)

        # 근무 유형 선택
        tk.Label(pop, text="근무 유형", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=30)
        combo = ttk.Combobox(pop, values=["주간", "오후", "야간", "휴무"], state="readonly", font=("Arial", 11))
        combo.set("주간")
        combo.pack(fill="x", padx=30, pady=(5, 30), ipady=3)

        # 컨트롤러에 저장 요청
        def save_new():
            sc_info = {
                "emp_id": emp["emp_id"],
                "working_day": cal.get_date(),
                "work_type_name": combo.get()
            }
            res = self.control.register_schedule(sc_info)
            if res == "OK":
                messagebox.showinfo("성공", "근무일이 등록되었습니다.", parent=pop)
                pop.destroy()
                self.render_modify_tab()
            elif res == "DUP":
                messagebox.showwarning("중복", "해당 날짜에 이미 근무일이 존재합니다.", parent=pop)
            else:
                messagebox.showerror("실패", "등록 중 오류가 발생했습니다.", parent=pop)

        tk.Button(pop, text="등록 완료", bg="#007bff", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=save_new).pack(fill="x", padx=30, ipady=5)

    # 근무일 수정/삭제 화면 렌더링
    def render_modify_tab(self):
        for w in self.tab_mod.winfo_children(): w.destroy()

        left_panel = tk.Frame(self.tab_mod, bg="white", width=350, relief="solid", bd=1)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(self.tab_mod, bg="white", relief="solid", bd=1)
        self.right_panel.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        tk.Label(left_panel, text="직원 목록 (내역 확인)", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=15, pady=15)
        tk.Frame(left_panel, bg="#dee2e6", height=1).pack(fill="x")

        emp_list = self.control.get_all_employees_for_schedule()
        for emp in emp_list:
            row = tk.Frame(left_panel, bg="white")
            row.pack(fill="x", pady=5)
            tk.Label(row, text=f"{emp['emp_name']} ({emp['dep_name']})", font=("Arial", 10), bg="white").pack(side="left", padx=10)
            
            tk.Button(row, text="근무일 확인", bg="#17a2b8", fg="white", font=("Arial", 9, "bold"), relief="flat", cursor="hand2",
                      command=lambda e=emp: self.show_emp_schedule_detail(e)).pack(side="right", padx=10)

        self.show_empty_schedule_detail()

    def show_empty_schedule_detail(self):
        for w in self.right_panel.winfo_children(): w.destroy()
        tk.Label(self.right_panel, text="왼쪽에서 직원을 선택해 근무일을 확인하세요.", font=("Arial", 11), bg="white", fg="gray").pack(expand=True)

    def show_emp_schedule_detail(self, emp):
        for w in self.right_panel.winfo_children(): w.destroy()

        header = tk.Frame(self.right_panel, bg="#f8f9fa")
        header.pack(fill="x")
        tk.Label(header, text=f"[{emp['emp_name']}] 님의 근무 일정 내역", font=("Arial", 13, "bold"), bg="#f8f9fa", fg="#212529").pack(anchor="w", padx=20, pady=15)

        cols = tk.Frame(self.right_panel, bg="white")
        cols.pack(fill="x", padx=20, pady=5)
        tk.Label(cols, text="날짜", font=("Arial", 10, "bold"), bg="white", width=15, anchor="w").pack(side="left")
        tk.Label(cols, text="유형", font=("Arial", 10, "bold"), bg="white", width=10, anchor="w").pack(side="left")
        tk.Label(cols, text="관리", font=("Arial", 10, "bold"), bg="white", width=15).pack(side="right")
        tk.Frame(self.right_panel, bg="#dee2e6", height=2).pack(fill="x", padx=20)

        # DB에서 해당 직원의 근무일 정보 가져오기
        schedules = self.control.get_emp_schedules(emp["emp_id"])
        if not schedules:
            tk.Label(self.right_panel, text="등록된 근무 일정이 없습니다.", font=("Arial", 11), bg="white", fg="#e64980").pack(pady=30)
            return

        list_canvas = tk.Canvas(self.right_panel, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=list_canvas.yview)
        scroll_frame = tk.Frame(list_canvas, bg="white")
        
        scroll_frame.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        list_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=450)
        list_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        list_canvas.configure(yscrollcommand=scrollbar.set)

        # 근무일 정보 반복문 출력
        for sc in schedules:
            row = tk.Frame(scroll_frame, bg="white")
            row.pack(fill="x", pady=5)
            tk.Label(row, text=str(sc["working_day"]), font=("Arial", 11), bg="white", width=15, anchor="w").pack(side="left")
            
            # 근무 유형별 색상 적용
            color = "#007bff" if sc["work_type_name"]=="주간" else "#28a745" if sc["work_type_name"]=="오후" else "#dc3545"
            tk.Label(row, text=sc["work_type_name"], font=("Arial", 10, "bold"), bg="white", fg=color, width=10, anchor="w").pack(side="left")

            btn_frame = tk.Frame(row, bg="white")
            btn_frame.pack(side="right")
            
            # [수정] 및 [삭제] 버튼
            tk.Button(btn_frame, text="수정", bg="#ffc107", fg="#212529", font=("Arial", 9, "bold"), relief="flat", cursor="hand2", 
                      command=lambda s=sc, e=emp: self.open_modify_popup(s, e)).pack(side="left", padx=2)
            tk.Button(btn_frame, text="삭제", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), relief="flat", cursor="hand2", 
                      command=lambda sid=sc["sc_id"], e=emp: self.click_delete(sid, e)).pack(side="left", padx=2)
            
            tk.Frame(scroll_frame, bg="#f1f3f5", height=1).pack(fill="x")

    # 기존 일정을 변경하는 팝업창 생성
    def open_modify_popup(self, sc, emp):
        pop = tk.Toplevel(self.parent_frame.winfo_toplevel())
        pop.title("근무일 수정")
        pop.geometry("300x350")
        pop.configure(bg="white")
        pop.attributes("-topmost", True)

        tk.Label(pop, text=f"일정 수정", font=("Arial", 14, "bold"), bg="white").pack(pady=20)

        # 기존 날짜로 기본 셋팅
        tk.Label(pop, text="날짜 선택", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=30)
        cal = CustomDateEntry(pop, width=12, date_pattern='yyyy-mm-dd', font=("Arial", 11))
        cal.set_date(sc["working_day"])
        cal.pack(fill="x", padx=30, pady=(5, 15), ipady=3)

        # 기존 유형으로 기본 셋팅
        tk.Label(pop, text="근무 유형", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=30)
        combo = ttk.Combobox(pop, values=["주간", "오후", "야간", "휴무"], state="readonly", font=("Arial", 11))
        combo.set(sc["work_type_name"])
        combo.pack(fill="x", padx=30, pady=(5, 30), ipady=3)

        def save_modify():
            sc_info = {
                "sc_id": sc["sc_id"], # 근무일 ID 전달
                "working_day": cal.get_date(),
                "work_type_name": combo.get()
            }
            if self.control.modify_schedule(sc_info):
                messagebox.showinfo("성공", "수정되었습니다.", parent=pop)
                pop.destroy()
                self.show_emp_schedule_detail(emp) # 수정 후 화면 새로고침
            else:
                messagebox.showerror("실패", "수정에 실패했습니다.", parent=pop)

        tk.Button(pop, text="수정 완료", bg="#ffc107", fg="#212529", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=save_modify).pack(fill="x", padx=30, ipady=5)

    # 삭제 버튼 클릭 시 처리
    def click_delete(self, sc_id, emp):
        if messagebox.askyesno("삭제 확인", "정말 이 근무 일정을 삭제하시겠습니까?"):
            if self.control.remove_schedule(sc_id):
                messagebox.showinfo("삭제", "성공적으로 삭제되었습니다.")
                self.show_emp_schedule_detail(emp) # 삭제 후 화면 새로고침


# [일반 직원용] 본인의 한 달 근무일과 휴가를 달력 형태로 열람하는 UI 클래스
class EmpSchUI:
    def __init__(self, parent_frame, user_id):
        print(f"[MainUI] 일반 직원({user_id}) 근무일 조회 화면으로 전환됩니다.")
        self.parent_frame = parent_frame
        self.user_id = user_id
        self.control = ScheduleControl()
        
        # 접속 시점의 오늘 날짜 기준으로 초기 달력 년/월 세팅
        today = datetime.datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        
        self.draw_ui()

    # 근무 일정 달력 화면 구성 메서드
    def draw_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        main_container = tk.Frame(self.parent_frame, bg="#f4f6f9")
        main_container.pack(fill="both", expand=True, padx=30, pady=30)

        card = tk.Frame(main_container, bg="white", relief="flat")
        card.pack(fill="both", expand=True)

        tk.Label(card, text="[EmpSchUI] 나의 근무 일정", font=("Arial", 16, "bold"), bg="white", fg="#212529").pack(anchor="w", padx=20, pady=(20, 10))

        header_frame = tk.Frame(card, bg="white")
        header_frame.pack(fill="x", pady=10)

        tk.Button(header_frame, text="◀", font=("Arial", 12), bg="white", relief="flat", cursor="hand2", command=self.prev_month).pack(side="left", padx=(100, 20))
        self.lbl_ym = tk.Label(header_frame, text=f"{self.current_year}년 {self.current_month}월", font=("Arial", 14, "bold"), bg="white", width=15)
        self.lbl_ym.pack(side="left")
        tk.Button(header_frame, text="▶", font=("Arial", 12), bg="white", relief="flat", cursor="hand2", command=self.next_month).pack(side="left", padx=(20, 0))

        self.cal_frame = tk.Frame(card, bg="white")
        self.cal_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.render_calendar()

    # 이전 달로 이동
    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.render_calendar()

    # 다음 달로 이동
    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.render_calendar()

    # DB 정보를 바탕으로 달력과 근무일 데이터를 화면에 렌더링하는 메서드
    def render_calendar(self):
        self.lbl_ym.config(text=f"{self.current_year}년 {self.current_month}월")
        
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        days = ["월", "화", "수", "목", "금", "토", "일"]
        for col, day in enumerate(days):
            fg_color = "red" if day == "일" else "blue" if day == "토" else "#495057"
            tk.Label(self.cal_frame, text=day, font=("Arial", 11, "bold"), bg="#f8f9fa", fg=fg_color, relief="solid", bd=1).grid(row=0, column=col, sticky="nsew", ipady=5)
            self.cal_frame.grid_columnconfigure(col, weight=1)

        # 컨트롤러를 통해 해당 월의 내 근무일 정보 가져오기
        my_schedule = self.control.get_my_schedule(self.user_id, self.current_year, self.current_month)

        # 근무 유형에 따른 예쁜 UI 색상 매핑
        type_colors = {
            "주간": {"bg": "#e7f5ff", "fg": "#1864ab"}, 
            "오후": {"bg": "#ebfbee", "fg": "#2b8a3e"}, 
            "야간": {"bg": "#fff0f6", "fg": "#a61e4d"}, 
            "휴무": {"bg": "#f8f9fa", "fg": "#868e96"}, 
            "휴가": {"bg": "#fff4e6", "fg": "#d9480f"}  
        }

        cal_data = calendar.monthcalendar(self.current_year, self.current_month)
        
        for row_idx, week in enumerate(cal_data):
            self.cal_frame.grid_rowconfigure(row_idx + 1, weight=1)
            for col_idx, day_num in enumerate(week):
                cell_frame = tk.Frame(self.cal_frame, bg="white", relief="solid", bd=1)
                cell_frame.grid(row=row_idx + 1, column=col_idx, sticky="nsew")

                # day_num이 0이면 빈 칸 (해당 월에 속하지 않는 날짜)
                if day_num != 0:
                    day_fg = "red" if col_idx == 6 else "blue" if col_idx == 5 else "black"
                    tk.Label(cell_frame, text=str(day_num), font=("Arial", 10), bg="white", fg=day_fg).pack(anchor="ne", padx=5, pady=2)

                    # 가져온 내 근무일 딕셔너리에 해당 일자 데이터가 있으면 박스 그려줌
                    if day_num in my_schedule:
                        work_type = my_schedule[day_num]
                        colors = type_colors.get(work_type, {"bg": "#f1f3f5", "fg": "black"})
                        
                        tk.Label(cell_frame, text=work_type, font=("Arial", 10, "bold"), bg=colors["bg"], fg=colors["fg"]).pack(fill="x", padx=3, pady=(5, 0), ipady=3)