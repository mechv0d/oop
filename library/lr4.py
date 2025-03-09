class Product:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    @property
    def name(self): return self.__name

    @property
    def price(self): return self.__price

    def __repr__(self):
        return f"Product(name='{self.__name}', price={self.__price})"


class ProductListManager:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def display_products(self):
        if not self.__products:
            print("Список продуктов пуст.")
        else:
            for product in self.__products:
                print(product)

    @staticmethod
    def find_max_price_product_2d(product_matrix):
        if not product_matrix:
            print("Двумерный список продуктов пуст.")
            return None

        max_p = None
        max_price = -1  # Initialize with negative price

        for row in product_matrix:
            if not row:
                continue
            for product in row:
                if product.__price > max_price:
                    max_price = product.__price
                    max_p = product

        if max_p is None:
            print("Двумерный список продуктов не содержит ни одного продукта")
        return max_p


# Пример использования
# 1. Работа с одномерным списком
product_manager = ProductListManager()

product1 = Product("Laptop", 1200.00)
product2 = Product("Mouse", 25.00)
product3 = Product("Keyboard", 75.00)

product_manager.add_product(product1)
product_manager.add_product(product2)
product_manager.add_product(product3)

print("Одномерный список продуктов:")
product_manager.display_products()

# 2. Работа с двумерным списком
product_matrix = [
    [Product("A", 10), Product("B", 20)],
    [Product("C", 30), Product("D", 40)],
    [Product("E", 50), Product("F", 60)],
]

product_matrix2 = [
    [],  # Empty row
    [Product("A", 10)],
    [Product("B", 20), Product("C", 30)]
]

# 3. Поиск продукта с максимальной ценой в двумерном списке
max_product = product_manager.find_max_price_product_2d(product_matrix)
if max_product:
    print("\nПродукт с максимальной ценой в двумерном списке:", max_product)

max_product2 = product_manager.find_max_price_product_2d(product_matrix2)
if max_product2:
    print("\nПродукт с максимальной ценой в product_matrix2:", max_product2)

# 4. Обработка пустого списка
empty_matrix = []
max_product_empty = product_manager.find_max_price_product_2d(empty_matrix)

empty_matrix_with_empty_rows = [[], [], []]
max_product_empty2 = product_manager.find_max_price_product_2d(empty_matrix_with_empty_rows)

matrix_with_no_products = [[], [], []]
max_product_no_products = product_manager.find_max_price_product_2d(matrix_with_no_products)
