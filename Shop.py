from game_units import Character
from item_storage import *


class Shop:
    """класс магазина с методами взаимодействия с магазином
    name
        имя магазина, тип: строка
    assortment
        ассортимент магазина, тип: список из Item"""

    def __init__(self, name: str, assortment: list[Item]):
        self.name = name
        self.assortment = assortment

    def show_items(self):
        """метод для показа всех вещей который есть в магазине с их ценой"""
        print(f"добро пожаловать в магазин {self.name}!")
        print("в продаже:")
        for i in range(len(self.assortment)):
            print(f"{i}, {self.assortment[i].name}: {self.assortment[i].price} монет")

    def buy_item(self, character: Character, item_index: str):
        """метод для покупки предмета по индексу и выводом баланса персонажа
        character
            персонаж который покупает предмет
        item_index
            индекс предмета, тип: строка
        """
        if not item_index.isdigit():
            print("Нужно ввести номер предмета числом!")
            return

        idx = int(item_index)

        if 0 <= idx < len(self.assortment):
            item_to_buy = self.assortment[idx]
            if character.gold >= item_to_buy.price:
                character.gold -= item_to_buy.price
                character.add_item(item_to_buy)
                print(f"вы купили {item_to_buy.name}, ваш баланс {character.gold}")
            else:
                # print("не хватает денег")
                print(f"недостаточно золота, ваш баланс: {character.gold}")
        else:
            print("предмета с таким номером нет")

    def sell_item(self, character: Character, item_to_sell: Item):
        """метод для продажи предмета за половину его цены
        character
            персонаж который продает предмет
        item_to_sell
            предмет для продажи"""
        if item_to_sell in character.inventory:
            revenue = item_to_sell.price // 2
            character.gold += revenue
            character.inventory.remove(item_to_sell)
            print(f"персонаж получил: {revenue} золота, баланс: {character.gold}")
            self.assortment.append(item_to_sell)
        else:
            print("предмета нет в инвентаре")
