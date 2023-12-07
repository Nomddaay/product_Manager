import os
import category as Category 
import pandas as pd

class Keep:
    def __init__(self):
        self.categories = []
        self.sort_id_ascending = True
        self.filename = "product_Manager/categories.csv"
        self.load_from_csv()

    def add_category(self, category):
        if not category.category_id:
            category.category_id = self.get_next_category_id()
        self.categories.append(category)
        self.save_to_csv()
    
    def update_category(self, category_id, new_name):
        for category in self.categories:
            if category.category_id == category_id:
                category.name = new_name
                break
        self.save_to_csv()

    def delete_category(self, category_id):
        self.categories = [category for category in self.categories if category.category_id != category_id]
        self.save_to_csv()

    def display_categories(self):
        return self.categories

       

    def save_to_csv(self):
        # Kiểm tra nếu thư mục không tồn tại, tạo mới nó
        if not os.path.exists(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename))

        # Tạo DataFrame và lưu vào file CSV
        data = {
            'CategoryID': [category.category_id for category in self.categories],
            'Name': [category.name for category in self.categories],
            'ParentID': [category.parent_id for category in self.categories],
        }

        df = pd.DataFrame(data)
        df.to_csv(self.filename, index=False)
    
    def load_from_csv(self):
        try:
            df = pd.read_csv(self.filename, encoding='latin1')
            self.categories = [Category.Category(row['CategoryID'], row['Name'],row['ParentID']) for _, row in df.iterrows()]
        except FileNotFoundError:
            pass

    def get_next_category_id(self):
        return max([category.category_id for category in self.categories], default=0) + 1
    
    def sort_by_id(self):
        self.sort_id_ascending = not self.sort_id_ascending

        self.categories = sorted(self.categories, key=lambda x: x.category_id, reverse=not self.sort_id_ascending)
        self.save_to_csv()
    
    def sort_by_name(self):
        self.categories = sorted(self.categories, key=lambda x: x.name)
        self.save_to_csv()

        