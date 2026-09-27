from dataclasses import dataclass, field


@dataclass
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

    name: str
    description: str
    price: int
    effect_value: int
    stackable: bool = True
    quantity: int = 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(unsafe_hash=True)
class Consumable(Item):
    """класс расходуемых предметов
    effect_type
        тип эффекта
    effect_value
        величина эффекта
    """
    effect_type: str = ""
    duration: int = 0

    def __str__(self):
        return (
            f"{self.name}, {self.description}, {self.price}, {self.effect_value},"
            f" {self.effect_type}, {self.stackable}, {self.quantity}"
        )

    def __repr__(self):
        return f"<{self.name} ({self.effect_value})>"


@dataclass(unsafe_hash=True)
class Equipment(Item):
    """класс снаряжения
    durability_value
        кол-во едениц снаряжения
    equipment_type
        тип желаемого снаряжения(шлем, нагрудник, поножи, обувь)"""

    equipment_type: str = ""
    durability_value: int = 100

    def __repr__(self):
        return f"<{self.name} ({self.effect_value})>"

    def __str__(self):
        return f"{self.name}, {self.description}, {self.price}, {self.durability_value}"



armor = Equipment("броня", "дает 50 брони", "нагрудник", 250, 50, 25)
potion = Consumable("фласка", "восстанавливает 30 здоровья", 95, "лечение", 40)

