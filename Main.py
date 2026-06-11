import tkinter as tk
from Boundary.Auth_Boundary import LoginUI

# 프로그램의 메인 진입점
if __name__ == "__main__":
    root = tk.Tk()
    
    app = LoginUI(root)
    
    root.mainloop()