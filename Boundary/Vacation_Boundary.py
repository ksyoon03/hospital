import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Control.Vacation_Control import *

class CustomDateEntry(DateEntry):
    def _focus_out(self, event):
        pass

# [관리자용] 직원들이 올린 휴가 신청 리스트를 조회하고 승인/반려하는 UI
class VacationUI:
    def __init__(self, parent_frame):
        print("[MainUI] 화면 크기에 반응하는 VacationUI 화면으로 전환됩니다.")
        self.parent_frame = parent_frame
        self.control = VacationControl()
        self.selected_vac = None # 휴가 신청서 정보
        self.draw_ui()

    def draw_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        main_container = tk.Frame(self.parent_frame, bg="#f4f6f9")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        left_panel = tk.Frame(main_container, bg="white", width=400, relief="solid", bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(main_container, bg="white", relief="solid", bd=1)
        self.right_panel.pack(side="left", fill="both", expand=True)

        tk.Label(left_panel, text="📄 직원 휴가 신청 목록", font=("Arial", 12, "bold"), bg="white", fg="#495057").pack(anchor="w", padx=15, pady=15)
        tk.Frame(left_panel, bg="#e9ecef", height=1).pack(fill="x")

        list_container = tk.Frame(left_panel, bg="white")
        list_container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(list_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=380)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.show_vacation_list() # DB에서 목록 불러오기
        self.show_empty_detail()

    # 컨트롤러에서 가공된 휴가 신청 리스트를 받아와 출력하는 메서드
    def show_vacation_list(self, status="all"):
        print("[VacationUI] show_vacation_list() 호출 -> 화면에 목록 렌더링")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        vac_list = self.control.get_vacation_list()

        for vac in vac_list:
            card = tk.Frame(self.scrollable_frame, bg="white", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
            card.pack(fill="x", pady=5, padx=5)

            def make_click_handler(v):
                return lambda e: self.show_detail(v)

            def bind_click(widget, handler):
                widget.bind("<Button-1>", handler)
                for child in widget.winfo_children():
                    child.bind("<Button-1>", handler)

            top_row = tk.Frame(card, bg="white")
            top_row.pack(fill="x", padx=10, pady=(10, 5))

            info_text = f"{vac.get('emp_name', '이름미상')}  {vac.get('dep_name', '부서미상')} / 일반직원"
            tk.Label(top_row, text=info_text, font=("Arial", 11, "bold"), bg="white", fg="#212529").pack(side="left")

            status_colors = {
                "대기중": {"bg": "#fff3cd", "fg": "#856404"},
                "승인됨": {"bg": "#d4edda", "fg": "#155724"},
                "거절됨": {"bg": "#f8d7da", "fg": "#721c24"}
            }
            colors = status_colors.get(vac["status"], {"bg": "#e2e3e5", "fg": "#383d41"})
            
            badge_text = "⏱️ 대기중" if vac["status"] == "대기중" else ("✔️ 승인됨" if vac["status"] == "승인됨" else "❌ 거절됨")
            tk.Label(top_row, text=badge_text, font=("Arial", 9, "bold"), bg=colors["bg"], fg=colors["fg"], padx=8, pady=2).pack(side="right")

            bottom_row = tk.Frame(card, bg="white")
            bottom_row.pack(fill="x", padx=10, pady=(0, 10))
            
            # 종류와 날짜, 소요기간 표시
            date_text = f"[{vac['vac_type']}] {vac['start_date']} ~ {vac['end_date']} ({vac['duration']})"
            tk.Label(bottom_row, text=date_text, font=("Arial", 9), bg="white", fg="#6c757d").pack(side="left")

            bind_click(card, make_click_handler(vac))

    def show_empty_detail(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        tk.Label(self.right_panel, text="상세 정보 및 처리", font=("Arial", 12, "bold"), bg="white", fg="#495057").pack(anchor="w", padx=20, pady=15)
        tk.Frame(self.right_panel, bg="#e9ecef", height=1).pack(fill="x")

        empty_frame = tk.Frame(self.right_panel, bg="white")
        empty_frame.pack(expand=True)
        tk.Label(empty_frame, text="👤", font=("Arial", 40), bg="white", fg="#ced4da").pack(pady=(0, 10))
        tk.Label(empty_frame, text="왼쪽 목록에서 휴가 신청 건을 선택해주세요.\n상세 정보를 확인하고 승인/거절 처리를 할 수 있습니다.", 
                 font=("Arial", 11), bg="white", fg="#868e96", justify="center").pack()

    # 리스트에서 특정 휴가 건 클릭 시 상세 사유와 승인/거절 버튼을 노출하는 메서드
    def show_detail(self, vac):
        self.selected_vac = vac
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        tk.Label(self.right_panel, text="상세 정보 및 처리", font=("Arial", 12, "bold"), bg="white", fg="#495057").pack(anchor="w", padx=20, pady=15)
        tk.Frame(self.right_panel, bg="#e9ecef", height=1).pack(fill="x")

        content = tk.Frame(self.right_panel, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=30)

        info_font = ("Arial", 11)
        tk.Label(content, text="신청자 정보", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=f"{vac['emp_name']} ({vac['dep_name']} / {vac['role']})", font=info_font, bg="white", fg="#495057").pack(anchor="w", pady=(0, 15))

        tk.Label(content, text="휴가 기간 및 종류", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=f"[{vac['vac_type']}] {vac['start_date']} ~ {vac['end_date']} (총 {vac['duration']})", font=info_font, bg="white", fg="#495057").pack(anchor="w", pady=(0, 15))

        tk.Label(content, text="현재 상태", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(content, text=vac["status"], font=info_font, bg="white", fg="#007bff" if vac["status"]=="대기중" else "#495057").pack(anchor="w", pady=(0, 20))

        # 현재 "대기중" 상태일 때만 승인/거절 폼 표시
        if vac["status"] == "대기중":
            tk.Label(content, text="거절 사유 입력 (거절 시 필수)", font=("Arial", 10, "bold"), bg="white", fg="#e64980").pack(anchor="w", pady=(10, 5))
            self.text_reason = tk.Text(content, height=4, font=("Arial", 10), relief="solid", bd=1)
            self.text_reason.pack(fill="x", pady=(0, 20))

            btn_frame = tk.Frame(content, bg="white")
            btn_frame.pack(fill="x")
            # 승인 버튼 클릭 시 click_approve 실행
            tk.Button(btn_frame, text="승인", bg="#28a745", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", 
                      command=lambda: self.click_approve(vac["vac_id"])).pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=8)
            # 거절 버튼 클릭 시 click_reject 실행
            tk.Button(btn_frame, text="거절", bg="#dc3545", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", 
                      command=lambda: self.click_reject(vac["vac_id"])).pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=8)
        else:
            # 이미 처리된 건은 추가 입력 없이 당시 처리 사유만 텍스트로 보여줌
            if vac["reason"]:
                tk.Label(content, text="처리 사유", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
                tk.Label(content, text=vac["reason"], font=info_font, bg="white", fg="#e64980").pack(anchor="w")

    # 승인 버튼 클릭 시 처리
    def click_approve(self, vac_id):
        # 컨트롤러에 승인 지시
        success = self.control.approve_vacation(vac_id, "admin")
        if success:
            messagebox.showinfo("승인 완료", "휴가 신청이 승인되었습니다.")
            self.show_vacation_list() # 리스트 갱신
            self.show_empty_detail()  # 처리 완료되었으므로 화면 리셋

    # 거절 버튼 클릭 시 처리
    def click_reject(self, vac_id):
        reason = self.text_reason.get("1.0", tk.END).strip()
        if not reason: # 사유를 안 적으면 반려 불가 방어 코드
            messagebox.showwarning("입력 필요", "거절 사유를 입력해주세요.")
            return
        
        success = self.control.reject_vacation(vac_id, "admin", reason)
        if success:
            messagebox.showinfo("거절 완료", "휴가 신청이 거절되었습니다.")
            self.show_vacation_list() 
            self.show_empty_detail()


# [일반 직원용] 휴가를 신청하는 화면 UI
class EmpVacationUI:
    def __init__(self, parent_frame, user_id):
        print(f"[MainUI] 일반 직원({user_id}) 휴가 신청 화면으로 전환됩니다.")
        self.parent_frame = parent_frame
        self.user_id = user_id
        self.control = VacationControl()
        
        # 신청 전 현재 직원의 정보와 잔여 휴가일수를 가져옴
        self.emp_info = Employee.find_by_id(self.user_id) 
        self.remain_vacation = self.emp_info.get("remain_vacation", 0) if self.emp_info else 0
        
        # 사용자가 화면에서 고르는 글자를 DB에 저장할 ID 매핑
        self.vac_types = {"연차 (종일)": 1, "반차": 2, "공가": 3, "병가": 4}
        
        self.draw_ui()

    # 휴가 신청서 작성 폼 화면 구성
    def draw_ui(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        container = tk.Frame(self.parent_frame, bg="#f4f6f9")
        container.pack(fill="both", expand=True, padx=40, pady=40)

        card = tk.Frame(container, bg="white", relief="solid", bd=1, highlightbackground="#dee2e6", highlightthickness=1)
        card.pack(fill="both", expand=True)

        header_frame = tk.Frame(card, bg="white")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        tk.Label(header_frame, text="📄 휴가 신청서", font=("Arial", 16, "bold"), bg="white", fg="#212529").pack(side="left")
        
        # 우측 상단 잔여 휴가일수 뱃지
        badge_frame = tk.Frame(header_frame, bg="#eef2fd", relief="flat")
        badge_frame.pack(side="right", ipady=5, ipadx=10)
        tk.Label(badge_frame, text=f"👤 나의 잔여 휴가: {self.remain_vacation}일", font=("Arial", 11, "bold"), bg="#eef2fd", fg="#4b49ac").pack()

        tk.Frame(card, bg="#dee2e6", height=1).pack(fill="x")

        # 신청서 입력 폼 영역 시작
        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # 1. 휴가 종류 선택
        tk.Label(form_frame, text="휴가 종류 *", font=("Arial", 11, "bold"), bg="white", fg="#495057").pack(anchor="w", pady=(0, 5))
        self.combo_type = ttk.Combobox(form_frame, values=list(self.vac_types.keys()), state="readonly", font=("Arial", 11))
        self.combo_type.set("연차 (종일)")
        self.combo_type.pack(fill="x", pady=(0, 20), ipady=5)

        # 2. 날짜 선택
        date_frame = tk.Frame(form_frame, bg="white")
        date_frame.pack(fill="x", pady=(0, 20))
        
        start_frame = tk.Frame(date_frame, bg="white")
        start_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(start_frame, text="시작일 *", font=("Arial", 11, "bold"), bg="white", fg="#495057").pack(anchor="w", pady=(0, 5))
        self.cal_start = CustomDateEntry(start_frame, width=12, date_pattern='yyyy-mm-dd', font=("Arial", 11))
        self.cal_start.pack(fill="x", ipady=5)

        end_frame = tk.Frame(date_frame, bg="white")
        end_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        tk.Label(end_frame, text="종료일 *", font=("Arial", 11, "bold"), bg="white", fg="#495057").pack(anchor="w", pady=(0, 5))
        self.cal_end = CustomDateEntry(end_frame, width=12, date_pattern='yyyy-mm-dd', font=("Arial", 11))
        self.cal_end.pack(fill="x", ipady=5)

        # 3. 휴가 사유 입력
        tk.Label(form_frame, text="사유 *", font=("Arial", 11, "bold"), bg="white", fg="#495057").pack(anchor="w", pady=(0, 5))
        self.text_reason = tk.Text(form_frame, height=5, font=("Arial", 11), relief="solid", bd=1)
        self.text_reason.pack(fill="x", pady=(0, 20))

        # 신청 버튼
        btn_frame = tk.Frame(card, bg="#f8f9fa")
        btn_frame.pack(fill="x", side="bottom")
        tk.Button(btn_frame, text="휴가 신청 확인", bg="#5c6bc0", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2", command=self.click_request).pack(side="right", padx=30, pady=20, ipadx=20, ipady=8)

    # 신청 버튼을 눌렀을 때 폼 데이터를 모아 컨트롤러로 전송하는 메서드
    def click_request(self):
        vac_type_name = self.combo_type.get()
        start_date = self.cal_start.get_date()
        end_date = self.cal_end.get_date()
        reason = self.text_reason.get("1.0", tk.END).strip()

        # 컨트롤러에 넘겨줄 딕셔너리 구조 생성
        req_info = {
            "emp_id": self.user_id,
            "vac_type_id": self.vac_types.get(vac_type_name, 1),
            "start_day": start_date,
            "end_day": end_date,
            "reason": reason
        }

        # 신청한 날짜 기간 계산
        request_days = (end_date - start_date).days + 1

        # 데이터 논리 오류 방어 코드
        if request_days <= 0:
            messagebox.showwarning("입력 오류", "종료일은 시작일 이후여야 합니다.")
            return
        if not reason:
            messagebox.showwarning("입력 오류", "사유를 입력해주세요.")
            return

        print(f"🖱️ [EmpVacationUI] click_request() 호출 -> 신청일수: {request_days}일")

        # 다이어그램 6: 컨트롤러를 통해 해당 직원의 잔여 휴가일수가 충분한지 검사
        if self.control.check_remain_vacation(self.user_id, request_days):
            # 다이어그램 8: 조건 만족 시 DB에 휴가 INSERT 요청
            success = self.control.request_vacation(req_info)
            if success:
                messagebox.showinfo("신청 완료", "휴가 신청이 성공적으로 완료되었습니다.")
                self.draw_ui() # 입력 폼 초기화
        else:
            # 잔여 휴가 부족 시 경고 알림 팝업
            messagebox.showwarning("신청 실패", "잔여 휴가가 부족합니다.")