import tkinter as tk
from tkinter import ttk, messagebox
from Control.Auth_Control import AuthControl
from Entity.Department_Entity import Department

# 로그인 화면 UI 클래스
class LoginUI:
    def __init__(self, root):
        self.root = root
        self.auth_control = AuthControl() # 로그인 로직을 처리할 컨트롤러 연결
        self.draw_ui()

    # 로그인 화면의 UI 위젯들을 배치하고 그리는 메서드
    def draw_ui(self):
        self.root.geometry("600x400")
        # 기존 화면에 있던 위젯들을 모두 지우고 초기화
        for widget in self.root.winfo_children():
            widget.destroy()

        card = tk.Frame(self.root, bg="white", padx=40, pady=40, relief="solid", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=440) 

        tk.Label(card, text="로그인", font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 20))

        tk.Label(card, text="아이디", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.entry_id = tk.Entry(card, font=("Arial", 12), relief="solid", bd=1)
        self.entry_id.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Label(card, text="비밀번호", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.entry_pw = tk.Entry(card, font=("Arial", 12), relief="solid", bd=1, show="*") # 비밀번호는 '*'로 표시
        self.entry_pw.pack(fill="x", pady=(5, 20), ipady=5)

        # 로그인 버튼 (클릭 시 click_login 메서드 실행)
        btn_login = tk.Button(card, text="로그인", bg="#007bff", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2", command=self.click_login)
        btn_login.pack(fill="x", ipady=8, pady=(0, 10))
        
        # 회원가입 버튼 (클릭 시 go_sign 메서드 실행)
        btn_sign = tk.Button(card, text="회원가입", bg="#f8f9fa", fg="#495057", font=("Arial", 11, "bold"), relief="solid", bd=1, cursor="hand2", command=self.go_sign)
        btn_sign.pack(fill="x", ipady=6)
        
    # 로그인 버튼 클릭 시 실행되는 이벤트 메서드
    def click_login(self):
        user_id = self.entry_id.get()
        user_pw = self.entry_pw.get()

        # 컨트롤러를 통해 DB 인증 시도
        if self.auth_control.authenticate(user_id, user_pw):
            # 인증 성공 시 권한을 확인하고 메인 화면으로 전환
            role = self.auth_control.check_permission(user_id)
            from Boundary.Main_Boundary import MainUI
            MainUI(self.root, role=role, user_id=user_id)
        else:
            # 인증 실패 시 경고창 팝업
            messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")

    # 회원가입 창으로 화면을 전환하는 메서드
    def go_sign(self): 
        SignUI(self.root)


# 회원가입 화면 UI 클래스
class SignUI:
    def __init__(self, root):
        self.root = root
        self.auth_ctrl = AuthControl() # 회원가입 로직을 처리할 컨트롤러 연결
        self.draw_ui()

    # 회원가입 화면의 UI 위젯들을 배치하고 그리는 메서드
    def draw_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        card = tk.Frame(self.root, bg="white", padx=40, pady=30, relief="solid", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=600)

        tk.Label(card, text="회원가입", font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 20))

        tk.Label(card, text="이름", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.e_name = tk.Entry(card, font=("Arial", 11), relief="solid", bd=1)
        self.e_name.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(card, text="아이디", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.e_id = tk.Entry(card, font=("Arial", 11), relief="solid", bd=1)
        self.e_id.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(card, text="비밀번호", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.e_pw = tk.Entry(card, font=("Arial", 11), relief="solid", bd=1, show="*")
        self.e_pw.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(card, text="비밀번호 확인", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.e_pwc = tk.Entry(card, font=("Arial", 11), relief="solid", bd=1, show="*")
        self.e_pwc.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(card, text="부서 선택", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w")
        self.cb_dep = ttk.Combobox(card, values=Department.get_all_department_names(), state="readonly", font=("Arial", 11))
        self.cb_dep.pack(fill="x", pady=(2, 10), ipady=4)
        if self.cb_dep['values']:
            self.cb_dep.current(0)

        self.v_admin = tk.BooleanVar()
        chk = tk.Checkbutton(card, text="관리자 계정으로 가입", variable=self.v_admin, bg="white", font=("Arial", 10))
        chk.pack(anchor="w", pady=(5, 15))

        # 가입하기 버튼
        btn_reg = tk.Button(card, text="가입하기", bg="#28a745", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2", command=self.clk_reg)
        btn_reg.pack(fill="x", ipady=6, pady=(0, 10))

        btn_back = tk.Button(card, text="뒤로가기", bg="#6c757d", fg="white", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=self.go_back)
        btn_back.pack(fill="x", ipady=6)

    # 가입하기 버튼 클릭 시 실행되는 이벤트 메서드
    def clk_reg(self):
        # 1. 사용자가 입력한 데이터 추출 및 양쪽 공백 제거
        uname = self.e_name.get().strip()
        uid = self.e_id.get().strip()
        upw = self.e_pw.get().strip()
        upwc = self.e_pwc.get().strip()
        dep = self.cb_dep.get()
        is_admin = self.v_admin.get()

        # 2. 필수 입력값 누락 검증
        if not uname or not uid or not upw or not upwc:
            messagebox.showwarning("입력 오류", "모든 항목을 입력해주세요.")
            return
            
        # 3. 비밀번호 일치 여부 검증
        if upw != upwc:
            messagebox.showwarning("오류", "비밀번호가 일치하지 않습니다.")
            return

        # 4. 검증 완료 후 딕셔너리로 묶어서 컨트롤러에 전달
        info = {'name': uname, 'id': uid, 'pw': upw, 'dep': dep, 'is_admin': is_admin}
        res = self.auth_ctrl.reg_user(info)

        # 5. 컨트롤러의 처리 결과에 따른 알림 및 화면 전환
        if res == "DUP":
            messagebox.showerror("중복", "이미 존재하는 아이디입니다.")
        elif res == "OK":
            messagebox.showinfo("성공", "회원가입이 완료되었습니다!")
            self.go_back() 
        else:
            messagebox.showerror("실패", "처리 중 오류가 발생했습니다.")
        
    # 다시 로그인 화면으로 돌아가는 메서드
    def go_back(self):
        LoginUI(self.root)