from lr_5.logger import base_logger as logger


class Food:
    __class_name = "Food"
    name: str
    calories: int
    weight: float  # grams
    ingredients: list[str]
    color: str

    food_value: ()

    def __init__(self, name, calories, weight, ingredients, color):
        logger.log(f"Создан родительский класс {self.__class_name} '{name}'")
        self.name = name
        self.calories = calories
        self.ingredients = ingredients
        self.weight = weight
        self.color = color  # for future graphical display
        self.ready = False
        self.food_value = lambda: int(self.calories / self.weight * 100)



    def prepare(self):
        logger.log(f"Метод prepare вызван у '{self.name}' ({self.__class_name})")
        self.ready = True
        logger.echo(self.name, f'приготовлено!')


    def __str__(self):
        return f"{self.name} ({self.calories} ккал.): {', '.join(self.ingredients)}. Пищевая ценность (100г.): {self.food_value()} ккал."


class Pizza(Food):
    __class_name = "Pizza"
    size: float

    def __init__(self, name, calories, weight, ingredients, color, size):
        super().__init__(name, calories, weight, ingredients, color)
        logger.log(f"Создан класс {self.__class_name} '{self.name}'")
        self.size = size


    def prepare(self):
        super().prepare()
        logger.log(f"Метод prepare вызван у '{self.name}' ({self.__class_name})")
        logger.echo(self.name, f"Размер пиццы: {self.size} см.")


class Salad(Food):
    __class_name = "Salad"
    dressing: str

    def __init__(self, name, calories, weight, ingredients, color, dressing):
        super().__init__(name, calories, weight, ingredients, color)
        logger.log(f"Создан класс {self.__class_name} '{self.name}'")
        self.dressing = dressing


    def prepare(self):
        super().prepare()
        logger.log(f"Метод prepare вызван у '{self.name}' ({self.__class_name})")
        logger.echo(self.name, f"Заправка добавлена: {self.dressing}")



pizza = Pizza("Маргарейти", 500, 300, ["тесто", "помидоры", "сыр"], "red", 30)
salad = Salad("Цезарь", 300, 80, ["салат", "куриная грудка", "гренки"], "green", "Майонез")

pizza.prepare()
salad.prepare()

logger.echo(None, str(pizza))
logger.echo(None, str(salad))

print(pizza.food_value())
