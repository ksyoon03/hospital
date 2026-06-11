import tkinter as tk
from tkinter import ttk, messagebox
from Control.Employee_Control import *

# 관리자용 직원 관리 UI 클래스
class EmployeeManagementUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.control = EmployeeControl() # 직원 데이터를 관리하는 컨트롤러 연결
        self.draw_ui()

    # 화면 기본 레이아웃 및 헤더를 그리는 메서드
    def draw_ui(self):
        # 기존 화면 내용 비우기
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        card = tk.Frame(self.parent_frame, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=30, pady=30)

        title_lbl = tk.Label(card, text="🏥 의료진 및 직원 명부", font=("Arial", 16, "bold"), bg="white")
        title_lbl.pack(anchor="w", pady=(25, 20), padx=20)

        header_frame = tk.Frame(card, bg="#f8f9fa", height=40)
        header_frame.pack(fill="x", padx=20)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="성명", font=("Arial", 11, "bold"), bg="#f8f9fa", width=15).pack(side="left", padx=10)
        tk.Label(header_frame, text="소속 부서", font=("Arial", 11, "bold"), bg="#f8f9fa", width=20).pack(side="left", padx=10)
        tk.Label(header_frame, text="근무 상태", font=("Arial", 11, "bold"), bg="#f8f9fa", width=15).pack(side="left", padx=10)
        tk.Label(header_frame, text="관리", font=("Arial", 11, "bold"), bg="#f8f9fa", width=15).pack(side="left", padx=10)

        tk.Frame(card, bg="#dee2e6", height=2).pack(fill="x", padx=20)

        # 컨트롤러에서 DB에 있는 모든 직원 리스트를 가져와서 화면에 출력
        emp_list = self.control.get_all_employee_info()
        self.show_employee_list(card, emp_list)

    # 리스트 데이터를 하나씩 행 형태로 출력하는 메서드
    def show_employee_list(self, parent_container, emp_list):
        for info in emp_list:
            row_frame = tk.Frame(parent_container, bg="white", height=55)
            row_frame.pack(fill="x", padx=20)
            row_frame.pack_propagate(False)

            # 성명과 부서명 출력
            tk.Label(row_frame, text=info["emp_name"], font=("Arial", 10), bg="white", width=15).pack(side="left", padx=10)
            tk.Label(row_frame, text=info["dep_name"], font=("Arial", 10), bg="white", width=20).pack(side="left", padx=10)
            
            status = info["emp_status"]
            status_frame = tk.Frame(row_frame, bg="white", width=150) 
            status_frame.pack(side="left", padx=10, fill="y")
            status_frame.pack_propagate(False)
            
            if status == "재직중":
                bg_color, fg_color = "#e7f5ff", "#1864ab" # 파란색
            elif status == "휴가중":
                bg_color, fg_color = "#fff4e6", "#d9480f" # 주황색
            else: # 휴직중
                bg_color, fg_color = "#f3f0ff", "#6741d9" # 보라색
            
            lbl_status = tk.Label(status_frame, text=status, font=("Arial", 9, "bold"), bg=bg_color, fg=fg_color)
            lbl_status.place(relx=0.5, rely=0.5, anchor="center", width=60, height=26)

            action_frame = tk.Frame(row_frame, bg="white", width=150)
            action_frame.pack(side="left", padx=10, fill="y")
            action_frame.pack_propagate(False)
            
            btn_edit = tk.Button(action_frame, text="정보 수정", font=("Arial", 9), bg="white", fg="#495057", 
                                 relief="solid", bd=1, cursor="hand2", 
                                 command=lambda e=info["emp_id"], n=info["emp_name"], d=info["dep_name"], s=status: self.click_update(e, n, d, s))
            btn_edit.place(relx=0.5, rely=0.5, anchor="center", width=70, height=30)

            tk.Frame(parent_container, bg="#f1f3f5", height=1).pack(fill="x", padx=20)

    # 정보 수정 버튼 클릭 시 팝업을 띄우는 메서드
    def click_update(self, emp_id, emp_name, current_dep, current_status):
        print(f"[EmployeeManagementUI] click_update() 호출 -> '{emp_name}'(ID: {emp_id}) 직원의 정보 수정 창을 엽니다!")
        
        # 새로운 팝업 창 생성
        edit_win = tk.Toplevel(self.parent_frame.winfo_toplevel())
        edit_win.title(f"직원 정보 수정 - {emp_name}")
        edit_win.geometry("320x350")
        edit_win.configure(bg="white")
        edit_win.grab_set()

        tk.Label(edit_win, text=f"{emp_name} 정보 수정", font=("Arial", 14, "bold"), bg="white").pack(pady=(20, 20))

        # 1. 소속 부서를 변경할 수 있는 콤보박스
        tk.Label(edit_win, text="소속 부서", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=40)
        combo_dep = ttk.Combobox(edit_win, values=Department.get_all_department_names(), state="readonly", font=("Arial", 11))
        combo_dep.set(current_dep) 
        combo_dep.pack(fill="x", padx=40, pady=(5, 20))

        # 2. 근무 상태를 변경할 수 있는 콤보박스
        tk.Label(edit_win, text="근무 상태", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=40)
        combo_status = ttk.Combobox(edit_win, values=["재직중", "휴가중", "휴직중"], state="readonly", font=("Arial", 11))
        combo_status.set(current_status) 
        combo_status.pack(fill="x", padx=40, pady=(5, 30))

        # 저장 버튼을 눌렀을 때 실행될 로직
        def save_changes():
            new_info = {
                "dep_name": combo_dep.get(),
                "emp_status": combo_status.get()
            }
            # 변경된 정보를 컨트롤러에 전달하여 DB 업데이트 수행
            self.control.update_employee(emp_id, new_info)
            messagebox.showinfo("수정 완료", f"{emp_name} 직원의 정보가 수정되었습니다.", parent=edit_win)
            edit_win.destroy()
            
            self.draw_ui() # 데이터가 변경되었으므로 메인 리스트를 다시 새로고침하여 그림

        # 저장 및 취소 버튼 영역
        btn_frame = tk.Frame(edit_win, bg="white")
        btn_frame.pack(fill="x", padx=40)
        
        tk.Button(btn_frame, text="취소", font=("Arial", 11), bg="#f8f9fa", relief="flat", cursor="hand2", 
                  command=edit_win.destroy).pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)
        tk.Button(btn_frame, text="저장", font=("Arial", 11, "bold"), bg="#007bff", fg="white", relief="flat", cursor="hand2", 
                  command=save_changes).pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=5)