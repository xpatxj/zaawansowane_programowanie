from magazine import Order, Product

product1 = Product("Laptop", 999.99)
order1 = Order("001", product1, 2)
order1.display_order_details()