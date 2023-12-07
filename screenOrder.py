import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime


class InvoiceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Danh sách hóa đơn")
        self.master.geometry("1000x500")

        # Tạo nhãn và ô tìm kiếm theo ngày hoặc tên
        self.search_label = tk.Label(self.master, text="Tìm kiếm:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        # Nút tìm kiếm hóa đơn theo ngày hoặc tên
        self.search_button = tk.Button(self.master, text="Tìm kiếm", command=self.search_invoice)
        self.search_button.grid(row=0, column=2, pady=10)

        # Bảng hiển thị danh sách hóa đơn
        self.invoice_table = ttk.Treeview(self.master, columns=("Name", "Price", "Quantity", "TotalPrice", "CreateDate"),
                                          show="headings")
        self.invoice_table.heading("Name", text="Tên sản phẩm")
        self.invoice_table.heading("Price", text="Giá")
        self.invoice_table.heading("Quantity", text="Số lượng")
        self.invoice_table.heading("TotalPrice", text="Tổng giá tiền")
        self.invoice_table.heading("CreateDate", text="Ngày tạo")
        self.invoice_table.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        self.load_invoices()

    def search_invoice(self):
        # Xóa dữ liệu hiện tại trong bảng
        for item in self.invoice_table.get_children():
            self.invoice_table.delete(item)

        # Lấy thông tin từ ô tìm kiếm
        search_term = self.search_entry.get().lower()

        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        with open("invoices.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if search_term in row["name"].lower() or search_term in row["createDate"].lower():
                    self.invoice_table.insert("", "end",
                                              values=(row["name"], row["price"], row["quantity"], row["totalPrice"],
                                                      row["createDate"]))

    def load_invoices(self):
        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        with open("invoices.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.invoice_table.insert("", "end",
                                          values=(row["name"], row["price"], row["quantity"], row["totalPrice"],
                                                  row["createDate"]))


class OrderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Đặt hàng")
        self.master.geometry("900x400")

        # Tạo các nhãn và ô nhập liệu
        self.quantity_label = tk.Label(self.master, text="Số lượng:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)

        self.quantity_entry = tk.Entry(self.master)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        # Tạo nút đặt hàng
        self.order_button = tk.Button(self.master, text="Đặt hàng", command=self.place_order)
        self.order_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Tạo nút hiển thị hóa đơn
        self.show_invoice_button = tk.Button(self.master, text="Hiển thị hóa đơn", command=self.show_invoice)
        self.show_invoice_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Tạo ô tìm kiếm sản phẩm
        self.search_label = tk.Label(self.master, text="Tìm kiếm sản phẩm:")
        self.search_label.grid(row=0, column=2, padx=10, pady=10)

        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=0, column=3, padx=10, pady=10)

        self.search_button = tk.Button(self.master, text="Tìm kiếm", command=self.search_product)
        self.search_button.grid(row=0, column=4, pady=10)


        # Tạo bảng hiển thị sản phẩm
        self.product_table = ttk.Treeview(self.master, columns=("ProductID", "Name", "Price"), show="headings")
        self.product_table.heading("ProductID", text="Product ID")
        self.product_table.heading("Name", text="Tên sản phẩm")
        self.product_table.heading("Price", text="Giá")
        self.product_table.grid(row=1, column=2, rowspan=4, columnspan=3, padx=10, pady=10)

        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        self.load_products()

    def place_order(self):
        # Lấy thông tin từ ô nhập liệu
        selected_item = self.product_table.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một sản phẩm từ bảng.")
            return

        product_id = self.product_table.item(selected_item, "values")[0]
        product_name = self.product_table.item(selected_item, "values")[1]
        quantity = self.quantity_entry.get()

        # Kiểm tra xem có thông tin nào bị bỏ trống hay không
        if not quantity:
            messagebox.showwarning("Lỗi", "Vui lòng nhập số lượng.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Số lượng phải là một số nguyên dương.")
        except ValueError:
            messagebox.showwarning("Lỗi", "Số lượng không hợp lệ.")
            return

        # Lấy giá của sản phẩm từ file CSV
        price = self.get_product_price(product_id)

        # Tính tổng giá tiền
        total_price = quantity * price

        # Lưu hóa đơn vào file CSV
        date_ordered = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("invoices.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([product_name, price, quantity, total_price, date_ordered])

        # Hiển thị thông báo xác nhận
        message = f"Đã đặt hàng:\nSản phẩm: {product_name}\nSố lượng: {quantity}\nTổng giá tiền: {total_price}\nNgày đặt hàng: {date_ordered}"
        messagebox.showinfo("Xác nhận đơn hàng", message)

        # Xóa nội dung của ô nhập liệu sau khi đặt hàng
        self.quantity_entry.delete(0, tk.END)

    def show_invoice(self):
        root = tk.Tk()
        app = InvoiceApp(root)
        root.mainloop()
        

    def search_product(self):
        # Xóa dữ liệu hiện tại trong bảng
        for item in self.product_table.get_children():
            self.product_table.delete(item)

        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        search_term = self.search_entry.get().lower()
        with open("products.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if search_term in row["Name"].lower():
                    self.product_table.insert("", "end", values=(row["ProductID"], row["Name"], row["Price"]))

    def load_products(self):
        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        with open("products.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.product_table.insert("", "end", values=(row["ProductID"], row["Name"], row["Price"]))

    def get_product_price(self, product_id):
        # Lấy giá của sản phẩm từ file CSV
        with open("products.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["ProductID"] == product_id:
                    return float(row["Price"])

    def invoices(self):
        InvoiceApp(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()
