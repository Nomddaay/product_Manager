import product as Product
import pandas as pd
class Store:
    def __init__(self):
        self.products = []
        self.sort_id_ascending = True
        self.filename = "products.csv"
        self.load_from_csv()

    def add_product(self, product):
        if not product.product_id:
            product.product_id = self.get_next_product_id()
        self.products.append(product)
        self.save_to_csv()

    def update_product(self, product_id, new_name, new_price):
        for product in self.products:
            if product.product_id == product_id:
                product.name = new_name
                product.price = new_price
                # product.quantity = new_quantity
                break
        self.save_to_csv()

    def delete_product(self, product_id):
        self.products = [product for product in self.products if product.product_id != product_id]
        self.save_to_csv()

    def display_products(self):
        return self.products

    def save_to_csv(self):
        data = {
            'ProductID': [product.product_id for product in self.products],
            'Name': [product.name for product in self.products],
            'Price': [product.price for product in self.products],
            'Quantity': [product.quantity for product in self.products],
        }

        df = pd.DataFrame(data)
        df.to_csv(self.filename, index=False)

    def load_from_csv(self):
        try:
            df = pd.read_csv(self.filename)
            self.products = [Product.Product(row['ProductID'], row['Name'], row['Price']) for _, row in df.iterrows()]
        except FileNotFoundError:
            pass  # Ignore if the file does not exist

    def get_next_product_id(self):
        return max([product.product_id for product in self.products], default=0) + 1

    def sort_by_id(self):
        self.sort_id_ascending = not self.sort_id_ascending

        # Sắp xếp tăng dần hoặc giảm dần tùy thuộc vào trạng thái hiện tại
        self.products = sorted(self.products, key=lambda x: x.product_id, reverse=not self.sort_id_ascending)
        self.save_to_csv()

    def sort_by_name(self):
        self.products = sorted(self.products, key=lambda x: x.name)
        self.save_to_csv()

    def sort_by_price(self):
        self.products = sorted(self.products, key=lambda x: x.price)
        self.save_to_csv()

    # def sort_by_quantity(self):
    #     self.products = sorted(self.products, key=lambda x: x.quantity)
    #     self.save_to_csv()

