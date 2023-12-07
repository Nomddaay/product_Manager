import tkinter as tk
from tkinter import messagebox
import csv
from screenProduct import screenProduct
from screenCategory import screenCategory
from screenHome import screenHome

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Coffee Product Manage Dashboard")

        # Tạo menu
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Home", command=self.show_home)
        file_menu.add_command(label="Page 1", command=self.pageProduct)
        file_menu.add_command(label="Page 2", command=self.show_page2)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

        menu_bar.add_cascade(label="Menu", menu=file_menu)
        self.config(menu=menu_bar)

        # Tạo frame chứa nội dung
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Gọi hàm để hiển thị trang chủ ban đầu
        self.show_home()

    def show_home(self):
        self.clear_frame()
        # label = tk.Label(self.main_frame, text="Welcome to the Home Page!", font=("Helvetica", 16))
        # label.pack(pady=20)
        home_screen = screenHome(self.main_frame)

    def pageProduct(self):
        self.clear_frame()
        screen1 = screenProduct(self.main_frame)

    def show_page2(self):
        self.clear_frame()
        screen2 = screenCategory(self.main_frame)

    def clear_frame(self):
        # Xóa nội dung của frame trước khi hiển thị trang mới
        for widget in self.main_frame.winfo_children():
            widget.destroy()

