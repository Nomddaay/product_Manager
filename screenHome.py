import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt

class screenHome(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        # Tạo một khu vực cuộn
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tạo một frame bên trong khu vực cuộn
        scroll_frame = tk.Frame(canvas)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        # Gọi hàm để hiển thị biểu đồ
        self.display_sales_chart(scroll_frame)

        # Thêm khu vực cuộn cho frame
        scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scroll_y.set)

        # Bắt sự kiện khi kích thước frame thay đổi
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Gắn frame vào khu vực cuộn
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Tạo nút cho biểu đồ tròn
        btn_pie = tk.Button(self, text="Hiển thị Biểu đồ Tròn", command=self.toggle_pie_chart)
        btn_pie.pack(side=tk.TOP)

        # Tạo nút cho biểu đồ cột
        btn_bar = tk.Button(self, text="Hiển thị Biểu đồ Cột", command=self.toggle_bar_chart)
        btn_bar.pack(side=tk.TOP)

        # Ẩn cả hai biểu đồ ban đầu
        self.canvas_pie.get_tk_widget().grid_forget()
        self.canvas_bar.get_tk_widget().grid_forget()

    def display_sales_chart(self, parent_frame):
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel("nuoc-uong.xlsx")

        # Lược bỏ cột 'month' khỏi DataFrame
        df_sales_only = df.drop('month', axis=1)

        # Tính tổng sales cho từng cột (mỗi món)
        total_sales = df_sales_only.sum(axis=0, skipna=True)

        # Tạo biểu đồ tròn
        plt.figure(figsize=(8, 8))
        plt.pie(total_sales, labels=total_sales.index, autopct='%1.1f%%', startangle=90, counterclock=False)
        plt.title('Tổng Sales Cho Các Món')

        # Tạo một FigureCanvasTkAgg để nhúng biểu đồ vào frame tkinter
        canvas_pie = FigureCanvasTkAgg(plt.gcf(), master=parent_frame)
        canvas_widget_pie = canvas_pie.get_tk_widget()
        canvas_widget_pie.grid(row=0, column=0, sticky=tk.NSEW)

        # Tạo DataFrame mới cho tháng 1
        df_month1 = df[df['month'] == 1]

        # Tạo biểu đồ cột cho tháng 1
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df_month1.columns[1:], df_month1.iloc[0, 1:], color=['skyblue', 'lightgreen', 'lightcoral', 'gold', 'orange', 'lightpink', 'lightblue', 'lightgray', 'yellow', 'lightseagreen'])
        ax.set_xlabel('Món')
        ax.set_ylabel('Doanh số bán')
        ax.set_title('Doanh số bán của các món trong tháng 1')
        ax.grid(True, linestyle="--")

        # Tạo một FigureCanvasTkAgg mới để nhúng biểu đồ cột vào frame tkinter
        canvas_bar = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas_widget_bar = canvas_bar.get_tk_widget()
        canvas_widget_bar.grid(row=1, column=0, sticky=tk.NSEW)

        # Đặt trọng số cột để có thể scroll được
        parent_frame.columnconfigure(0, weight=1)
        parent_frame.rowconfigure(0, weight=1)
        parent_frame.rowconfigure(1, weight=1)

        # Lưu trữ các biểu đồ để có thể thao tác trên chúng
        self.canvas_pie = canvas_pie
        self.canvas_bar = canvas_bar

    def toggle_pie_chart(self):
        # Ẩn biểu đồ cột nếu đang hiển thị, hiển thị nếu đang ẩn
        is_pie_visible = self.canvas_pie.get_tk_widget().winfo_ismapped()
        if is_pie_visible:
            self.canvas_pie.get_tk_widget().grid_forget()
        else:
            self.canvas_bar.get_tk_widget().grid_forget()  # Ẩn biểu đồ cột
            self.canvas_pie.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)

    def toggle_bar_chart(self):
        # Ẩn biểu đồ cột nếu đang hiển thị, hiển thị nếu đang ẩn
        is_bar_visible = self.canvas_bar.get_tk_widget().winfo_ismapped()
        if is_bar_visible:
            self.canvas_bar.get_tk_widget().grid_forget()
        else:
            self.canvas_pie.get_tk_widget().grid_forget()  # Ẩn biểu đồ tròn
            self.canvas_bar.get_tk_widget().grid(row=1, column=0, sticky=tk.NSEW)

        

if __name__ == "__main__":
    root = tk.Tk()
    app = screenHome(root)
    root.mainloop()
