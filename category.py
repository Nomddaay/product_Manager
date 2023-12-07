class Category:
    def __init__(self, category_id, name, parent_id: None):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id
    def display_info(self):
        return f"{self.category_id}\t{self.name}"