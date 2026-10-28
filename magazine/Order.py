from . import utils


class Order:
    def __init__(self, order_id, product, quantity):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity

    def calculate_total(self):
        return self.product.price * self.quantity

    def display_order_details(self):
        print(f"Order ID: {self.order_id}")
        print(f"Product: {self.product.name}")
        print(f"Quantity: {self.quantity}")
        print(f"Total Price: ${self.calculate_total():.2f}")
