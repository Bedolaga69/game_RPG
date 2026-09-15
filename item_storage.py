import random

from Items import *

ITEMS = {
    "regen_potion": Consumable(
        "длительное зелье здоровья",
        "дает регенерацию на 4 хода",
        150,
        "regeneration",
        10,
        3,
    ),
    "gold_pouch_small": Consumable(
        "маленький мешок золота", "дает 15 золота", 0, "gold", 15
    ),
    "gold_pouch_medium": Consumable(
        "среднй мешок золота", "дает 45 золота", 0, "gold", 45
    ),
    "gold_pouch_large": Consumable(
        "большой мешок золота", "дает 90 золота", 0, "gold", 90
    ),
    "heal_potion": Consumable(
        "зелье здоровья", "восстанавливает 30 здоровья", 95, "heal", 30
    ),
    "attack_potion": Consumable(
        "зелье урона", "дает +10 к урону", 150, "buff_attack", 10
    ),
    "defense_potion": Consumable(
        "зелье защиты", "дает +15 к защите", 100, "buff_defense", 15
    ),
    "sword": Equipment("меч", "дает 33 урона", "weapon", 300, 33, 33),
    "armor": Equipment("броня", "дает 50 брони", "armor", 50, 250, 25),
    "sword_of_heaven": Equipment(
        "меч небожитель", "дает 69 урона", "weapon", 500, 69, 69
    ),
    "chainmail": Equipment("нагрудник", "дает 33 брони", "armor", 200, 33, 33),
    "wooden_sword": Equipment("деревянный меч", "дает 5 урона", "weapon", 20, 5, 5),
    "golden_armor": Equipment("золотая броня", "дает 25 брони", "armor", 350, 25, 25),
    "master_sword": Equipment(
        "Меч Мастера", "легендарный меч из легенды о Зельде", "weapon", 1000, 55, 55
    ),
    "moonlight_sword": Equipment(
        "Лунный свет", "волшебный меч из Dark Souls", "weapon", 800, 48, 48
    ),
    "daedric_sword": Equipment(
        "Даэдрический меч", "убийца драконов из Skyrim", "weapon", 900, 52, 52
    ),
    "bustersword": Equipment(
        "Меч-бастер", "гигантская плита из Final Fantasy VII", "weapon", 1200, 70, 70
    ),
    "frostmourne": Equipment(
        "Ледяная Скорбь", "рунный меч Лича Короля (Warcraft)", "weapon", 1500, 85, 85
    ),
    "aerondight": Equipment(
        "Аэрондигхт", "меч ведьмака из The Witcher", "weapon", 1100, 60, 60
    ),
    "dragonplate_armor": Equipment(
        "Драконья броня", "лучшая кованая броня из Skyrim", "armor", 1200, 75, 75
    ),
    "elven_armor": Equipment(
        "Эльфийская броня",
        "лёгкая и прочная броня из Elder Scrolls",
        "armor",
        600,
        35,
        35,
    ),
    "orsimer_armor": Equipment(
        "Орсимерская броня", "броня орков из Skyrim", "armor", 700, 48, 48
    ),
    "paladin_armor": Equipment(
        "Паладинская броня", "святая броня из Diablo", "armor", 900, 55, 55
    ),
    "dark_souls_armor": Equipment(
        "Броня рыцаря", "классическая броня из Dark Souls", "armor", 750, 50, 50
    ),
    "witcher_armor": Equipment(
        "Ведьмачья броня", "броня школы Гриффина из The Witcher", "armor", 850, 45, 45
    ),
    "doom_armor": Equipment(
        "Прадорская броня", "броня Палача Рока из Doom", "armor", 1300, 80, 80
    ),
    "holy_chestplate": Equipment(
        "Святая кираса", "броня паладина из WoW", "armor", 1000, 65, 65
    ),
    "excalibur": Equipment(
        "Экскалибур", "легендарный меч короля Артура", "weapon", 2500, 100, 100
    ),
}


class LootTable:
    """класс для генерации предметов и добавления их в инвентарь"""

    def __init__(self, guaranteed_list: list[Item] | None = None):
        """guaranteed_list
        гарантированный список предметов для магазина
        значение по умолчанию — None"""
        if guaranteed_list is None:
            guaranteed_list = []
        self.loot_pool = {}
        self.guaranteed_list = guaranteed_list

    def add_drop(self, item_key, probability):
        """метод для добавления предметов в инвентарь по индексу
        item_key
            уникальный ключ предмета
        probability
            шанс выпадения предмета"""
        self.loot_pool[item_key] = probability

    def generate_loot(self, num_rolls=1) -> list[Item]:
        """Метод для генерации лута через независимые броски кубика
        num_rolls
            количество бросков кубика, по умолчанию 1
        list[Item]
            список сгенерированных предметов (включая гарантированные)"""
        loot_list = []
        loot_list.extend(self.guaranteed_list)

        for item_key, probability in self.loot_pool.items():
            if item_key not in ITEMS:
                continue

            for _ in range(num_rolls):
                if random.random() <= probability:
                    loot_list.append(ITEMS[item_key])

        return loot_list

    # def generate_loot(self, num_rolls=1) -> list[Item]:
    #     """метод для генерации лута через накопление шанса"""
    #     loot_list = []
    #     loot_list.extend(self.guaranteed_list)
    #     for item_key, probability in self.loot_pool.items():
    #         roll = random.random()
    #         cumulative_probability = 0
    #         for g in range(num_rolls):
    #             cumulative_probability += probability
    #             if roll <= cumulative_probability:
    #                 if item_key in ITEMS:
    #                     loot_list.append(ITEMS[item_key])
    #                 break
    #     return loot_list


shop_loot = LootTable([ITEMS["heal_potion"], ITEMS["defense_potion"]])
shop_loot.add_drop("sword", 0.5)
shop_loot.add_drop("armor", 0.4)
shop_loot.add_drop("attack_potion", 0.7)
shop_loot.add_drop("moonlight_sword", 0.04)
shop_loot.add_drop("daedric_sword", 0.05)
shop_loot.add_drop("elven_armor", 0.06)
shop_loot.add_drop("excalibur", 0.009)
shop_loot.add_drop("paladin_armor", 0.07)
shop_loot.add_drop("holy_chestplate", 0.08)


test = LootTable()
strong_enemy_loot = LootTable()

strong_enemy_loot.add_drop("heal_potion", 0.8)
strong_enemy_loot.add_drop("defense_potion", 0.4)
strong_enemy_loot.add_drop("sword", 0.1)
strong_enemy_loot.add_drop("armor", 0.08)
strong_enemy_loot.add_drop("wooden_sword", 0.2)
strong_enemy_loot.add_drop("chainmail", 0.3)
strong_enemy_loot.add_drop("gold_pouch_medium", 0.3)
strong_enemy_loot.add_drop("gold_pouch_large", 0.2)

test.add_drop("regen_potion", 0.4)
test.add_drop("heal_potion", 0.4)
test.add_drop("defense_potion", 0.3)
test.add_drop("sword", 0.08)
test.add_drop("armor", 0.06)
test.add_drop("gold_pouch_small", 0.3)
test.add_drop("gold_pouch_medium", 0.2)
test.add_drop("gold_pouch_large", 0.08)

enemy_loot = {
    "Гоблин": test,
    "Скелет": test,
    "Орк": strong_enemy_loot,
    "Темный Искатель": test,
    "Каменный Голем": strong_enemy_loot,
    "Вампир": strong_enemy_loot,
    "Древний Лич": strong_enemy_loot,  # мейби босс лут
}

# print(test.loot_pool)
# print(test.generate_loot())
# print(test.loot_pool)
# print(test.generate_loot(3))
# print(test.loot_pool)
# print(enemy_loot)
