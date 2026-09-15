class Item:
    """главный класс для всех игровых предметов
    name
        имя
    description
        описание
    item_type
        тип предмета
    price
        цена предмета"""

    def __init__(
        self,
        name,
        description,
        price,
        effect_value,
        stackable=True,
        quantity=1,
    ):
        """инициализирует базовый игровой предмет"""
        self.name = name
        self.description = description
        self.price = price
        self.stackable = stackable
        self.quantity = quantity
        self.effect_value = effect_value

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)


class Consumable(Item):
    """класс расходуемых предметов
    effect_type
        тип эффекта
    effect_value
        величина эффекта
    """

    def __init__(self, name, description, price, effect_type, effect_value, duration=0):
        """инициализирует расходуемый предмет"""
        super().__init__(name, description, price, effect_value)
        self.effect_type = effect_type
        self.duration = duration

    def __str__(self):
        return (
            f"{self.name}, {self.description}, {self.price}, {self.effect_value},"
            f" {self.effect_type}, {self.stackable}, {self.quantity}"
        )

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<{self.name} ({self.effect_value})>"


class Equipment(Item):
    """класс снаряжения
    durability_value
        кол-во едениц снаряжения
    equipment_type
        тип желаемого снаряжения(шлем, нагрудник, поножи, обувь)"""

    def __init__(
        self, name, description, equipment_type, price, effect_value, durability_value
    ):
        """инициализирует элемент снаряжения"""
        super().__init__(name, description, price, effect_value)
        self.durability_value = durability_value
        self.equipment_type = equipment_type

    def __repr__(self):
        return f"<{self.name} ({self.effect_value})>"

    def __str__(self):
        return f"{self.name}, {self.description}, {self.price}, {self.durability_value}"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)


armor = Equipment("броня", "дает 50 брони", "нагрудник", 250, 50, 25)
potion = Consumable("фласка", "восстанавливает 30 здоровья", 95, "лечение", 40)
"""вывод в консоль информации о чем либо(сейчас об снаряжении и зелье)"""
# print(armour)
# print(potion)
