import tkinter as tk
from tkinter import ttk, messagebox
from product import Product
from store import Store

class screenProduct:
    def __init__(self, master):
        self.master = master

        self.store = Store()
        self.create_widgets()

    def create_widgets(self):
        columns = ("ID", "Name", "Price")
        self.product_tree = ttk.Treeview(self.master, columns=columns, show="headings")

        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=150, anchor=tk.CENTER)
       
        self.product_tree.grid(row=8, column=0, columnspan=4, pady=10, padx=10)
        # Thêm nút sắp xếp theo ID và tên
        
        name_label = tk.Label(self.master, text="Product Name:")
        name_label.grid(row=2, column=0, sticky="E")

        self.name_entry = tk.Entry(self.master,bd=3)
        self.name_entry.grid(row=2, column=1)

        price_label = tk.Label(self.master, text="Product Price:")
        price_label.grid(row=3, column=0, sticky="E")

        self.price_entry = tk.Entry(self.master, bd=3)
        self.price_entry.grid(row=3, column=1)

        # quantity_label = tk.Label(self.master, text="Product Quantity:")
        # quantity_label.grid(row=4, column=0, sticky="E")

        # self.quantity_entry = tk.Entry(self.master,bd=3)
        # self.quantity_entry.grid(row=4, column=1)

        add_product_button = tk.Button(self.master, text="Add Product", command=self.add_product)
        add_product_button.grid(row = 5, column = 0,columnspan=1, pady=2)

        update_product_button = tk.Button(self.master, text="Update Product", command=self.update_product)
        update_product_button.grid(row=5, column=1,columnspan=1, pady=2)

        delete_product_button = tk.Button(self.master, text="Delete Product", command=self.delete_product)
        delete_product_button.grid(row=5, column=2,columnspan=1, pady=2)
         
        sort_by_id_button = tk.Button(self.master, text="Sort by ID", command=self.sort_by_id)
        sort_by_id_button.grid(row=6, column=0,columnspan=1, pady=2)

        sort_by_name_button = tk.Button(self.master, text="Sort by Name", command=self.sort_by_name)
        sort_by_name_button.grid(row=6, column=1,columnspan=1, pady=2)

        self.update_product_list()

    def update_product_list(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        for product in self.store.display_products():
            self.product_tree.insert("", "end", values=(product.product_id, product.name, product.price))

    def add_product(self):
        try:
            new_name = self.name_entry.get()
            new_price_str = self.price_entry.get()
            # new_quantity_str = self.quantity_entry.get()

            if not new_name or not new_price_str:
                messagebox.showwarning("Error", "Please fill in all fields.")
                return

            new_price = float(new_price_str)
            # new_quantity = int(new_quantity_str)

            new_product = Product(None, new_name, new_price)
            self.store.add_product(new_product)

            self.update_product_list()

            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            # self.quantity_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showwarning("Error", "Please enter valid numeric values for Price.")

    def update_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select a product to update.")
            return

        selected_index = self.product_tree.index(selected_item)
        selected_product = self.store.products[selected_index]

        new_name = self.name_entry.get()
        new_price_str = self.price_entry.get()
        # new_quantity_str = self.quantity_entry.get()

        if new_name:
            selected_product.name = new_name
        if new_price_str:
            selected_product.price = float(new_price_str)
        # if new_quantity_str:
        #     selected_product.quantity = int(new_quantity_str)

        self.store.save_to_csv()
        self.update_product_list()

        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        # self.quantity_entry.delete(0, tk.END)

    def sort_by_id(self):
        self.store.sort_by_id()
        self.update_product_list()

    def sort_by_name(self):
        self.store.sort_by_name()
        self.update_product_list()

    def delete_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select a product to delete.")
            return

        selected_index = self.product_tree.index(selected_item)
        selected_product = self.store.products[selected_index]

        confirmation = messagebox.askyesno(
            "Delete Product", f"Do you want to delete the selected product?\n{selected_product.display_info()}"
        )
        if confirmation:
            self.store.delete_product(selected_product.product_id)
            self.update_product_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = screenProduct(root)
    root.mainloop()
