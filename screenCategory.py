import tkinter as tk
from tkinter import ttk, messagebox
from category import Category
from keep import Keep

class screenCategory:
    def __init__(self, master):
        self.master = master
        self.keep = Keep()
        self.create_widgets()
        self.selected_subcategory_id = None

    def create_widgets(self):
        # Category Combobox
        category_label = tk.Label(self.master, text="Category:")
        category_label.grid(row=0, column=0, sticky="E")

        self.category_combobox = ttk.Combobox(self.master, values=["ĐỒ UỐNG", "THỨC ĂN"])
        self.category_combobox.grid(row=0, column=1, pady=5)
        self.category_combobox.bind("<<ComboboxSelected>>", self.update_subcategories)

        # Subcategory Combobox
        subcategory_label = tk.Label(self.master, text="Subcategory:")
        subcategory_label.grid(row=1, column=0, sticky="E")

        self.subcategory_combobox = ttk.Combobox(self.master, values=[])
        self.subcategory_combobox.grid(row=1, column=1, pady=5)
        self.subcategory_combobox.bind("<<ComboboxSelected>>", self.update_subcategories_and_parent_id)

        # Category Treeview and related widgets
        self.category_tree = ttk.Treeview(self.master, columns=("ID", "Name", "ParentID"), show="headings")
        for col in ["ID", "Name", "ParentID"]:
            self.category_tree.heading(col, text=col)
            self.category_tree.column(col, width=150, anchor=tk.CENTER)
        self.category_tree.grid(row=8, column=0, columnspan=4, pady=10, padx=10)

        self.name_label = tk.Label(self.master, text="Category Name:")
        self.name_entry = tk.Entry(self.master, bd=3)
        self.name_label.grid(row=2, column=0, sticky="E")
        self.name_entry.grid(row=2, column=1)

        self.add_category_button = tk.Button(self.master, text="Add Product", command=self.add_category)
        self.add_category_button.grid(row=6, column=0, columnspan=1, pady=2)
        self.update_category_button = tk.Button(self.master, text="Update Product", command=self.update_category)
        self.update_category_button.grid(row=6, column=1, columnspan=1, pady=2)
        self.delete_category_button = tk.Button(self.master, text="Delete Product", command=self.delete_category)
        self.delete_category_button.grid(row=6, column=2, columnspan=1, pady=2)

        self.sort_by_id_button = tk.Button(self.master, text="Sort by ID", command=self.sort_by_id)
        self.sort_by_id_button.grid(row=7, column=0, columnspan=1, pady=2)
        self.sort_by_name_button = tk.Button(self.master, text="Sort by Name", command=self.sort_by_name)
        self.sort_by_name_button.grid(row=7, column=1, columnspan=1, pady=2)
        self.update_category_list()

    def update_category_list(self):
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        for category in self.keep.display_categories():
            self.category_tree.insert("", "end", values=(category.category_id, category.name))    

    def update_subcategories(self, event):
        selected_category = self.category_combobox.get()

        if selected_category == "THỨC ĂN":
            subcategory_values = ["ĐỒ ĂN KÈM", "ĐỒ ĂN VẶT"]
        elif selected_category == "ĐỒ UỐNG":
            subcategory_values = ["CÀ PHÊ", "NƯỚC ÉP"]
        else:
            subcategory_values = []

        # Update subcategory_combobox values
        self.subcategory_combobox['values'] = subcategory_values
        # Set the default value to the first item in the list
        if subcategory_values:
            self.subcategory_combobox.set(subcategory_values[0])

    def update_subcategories_and_parent_id(self, event):
        
        pass        

    def add_category(self):
        try:
            new_name = self.name_entry.get()

            if not new_name:
                messagebox.showwarning("Error", "Please fill in all fields.")
                return

            # Thêm giá trị None cho parent_id
            new_category = Category(None, new_name, None)
            self.keep.add_category(new_category)

            self.update_category_list()

            self.name_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showwarning("Error", "Please enter valid numeric values for Price and Quantity.")

    def update_category(self):
        selected_item = self.category_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select a category to update.")
            return

        selected_index = self.category_tree.index(selected_item)
        selected_category = self.keep.categories[selected_index]

        new_name = self.name_entry.get()

        if new_name:
            selected_category.name = new_name

        self.keep.save_to_csv()
        self.update_category_list()

        self.name_entry.delete(0, tk.END)

    def sort_by_id(self):
        self.keep.sort_by_id()
        self.update_category_list()

    def sort_by_name(self):
        self.keep.sort_by_name()
        self.update_category_list()

    def delete_category(self):
        selected_item = self.category_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Please select a category to delete.")
            return

        selected_index = self.category_tree.index(selected_item)
        selected_category = self.keep.categories[selected_index]

        confirmation = messagebox.askyesno(
            "Delete category", f"Do you want to delete the selected category?\n{selected_category.display_info()}"
        )
        if confirmation:
            self.keep.delete_category(selected_category.category_id)
            self.update_category_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = screenCategory(root)
    root.mainloop()
