import random

from game_characters import *
from game_units import *
from item_storage import *
from Shop import *


class Game:
    def __init__(self, name, description):
        """инициализация полей класса
        name
            имя персонажа
        description
            описание
        is_running
            проверка на работает ли
        enemies
            список врагов
        characters_templates
            словарь с данными о персонаже
        current_player
            персонаж
        current_enemy
            враг"""
        self.shop = Shop("магазинчек", [])
        self.name = name
        self.description = description
        self.is_running = False
        self.enemies = []
        self.characters_templates = {}
        self.current_player = None
        self.current_enemy = None

    def start_game(self):
        """метод старта игры с выбором персонажа"""
        print("добро пожаловать в игру!")
        self.is_running = True
        self.characters_templates = {"1": Warrior, "2": Mage, "3": Archer}
        answer = input("выберите персонажа 1-3: воин - 1, маг - 2, лучник - 3 :")
        if answer in self.characters_templates:
            char_name = input("введите имя героя: ")
            ClassType = self.characters_templates[answer]
            self.current_player = ClassType(name=char_name)
            print(f"\nвы выбрали {self.current_player.name}")
            # print(f"по умолчанию у вас: {self.current_player.add_item(Consumable("зелье здоровья", "восстанавливает 30 здоровья",95, "heal", 30))}")
            # self.current_player.add_item(ITEMS["heal_potion"])
            # print(f"Вы получили стартовое снаряжение!")
        else:
            self.current_player = self.characters_templates["1"]("воин")
            print("некорректный выбор, по умолчанию выбран воин")
            # print(f"по умолчанию у вас: {self.current_player.add_item(Consumable("зелье здоровья", "восстанавливает 30 здоровья", 95, "heal", 30))}")
        self.current_player.add_item(ITEMS["heal_potion"], ITEMS["regen_potion"])
        print("Вы получили стартовое снаряжение!")
        self._create_default_enemies(10)
        self._start_battle_loop()

    def _create_default_enemies(self, count):
        """Приватный метод для создания набора врагов
        count
           количество врагов"""
        enemy_templates = [
            ("Гоблин", 28, 15, 4, 15),
            ("Скелет", 50, 20, 5, 25),
            ("Орк", 100, 30, 13, 50),
            ("Темный Искатель", 65, 41, 6, 35),
            ("Каменный Голем", 150, 20, 20, 60),
            ("Вампир", 110, 23, 10, 90),
            ("Древний Лич", 200, 50, 15, 300),
            # добавить разнообразных врагов, добавить голду с них и увел их кол-во
        ]

        for i in range(count):
            # Выбираем шаблон врага циклически
            template = enemy_templates[i % len(enemy_templates)]
            name, hp, atk, dfns, gold = template
            self.enemies.append(Enemy(name, hp, atk, dfns, gold))

        print(f"вы оглянулись и увидели {len(self.enemies)} врагов")

    def _start_battle_loop(self):
        """начало игрового лупа"""
        # надо поменять чутка код В НАЧАЛЕ
        counter = 0
        turn_counter = 1

        for enemy in self.enemies:
            while self.current_player.is_alive() and enemy.is_alive():
                print(f"ход {turn_counter}")
                is_player_acted = self._process_player_action(
                    enemy
                )  # Вызываем ход игрока

                if not is_player_acted:
                    rndm = random.randint(0, 3)
                    if rndm == 2:
                        print("вам удалось сбежать!!!!!")
                        break
                    else:
                        print("у вас не получилось сбежать, бой продолжается")

                if enemy.is_alive():  # проверка есть ли враги
                    self._process_enemy_turn(enemy)  # если есть, то атакуют
                self.current_player.update_effect()
                enemy.update_effect()
                turn_counter += 1

            if not self.current_player.is_alive():  # проверка на хп игрока
                break

            if not enemy.is_alive():
                counter += 1

        if self.current_player.is_alive():
            if counter == len(self.enemies):
                print("победа!!!")
            else:
                print("вам повезло выжить...")
        else:
            print("помир, скукожился, скропостижнулса")


    def start_shop_event(self):
        """открытие магазина для покупки предметов со своим шансом в магазине"""
        if random.random() < 0.5:
            self.shop.assortment = shop_loot.generate_loot()
            while True:
                answer = input("хотите зайти в магазин?\n 1 - да\n 2 - нет")
                if answer == "1":
                    answer_shop = input(
                        "что хотите сделать?"
                        "\n 1 - купить"
                        "\n 2 - продать"
                        "\n 3 - использовать предмет"
                    )
                    if answer_shop == "1":
                        # self.shop.assortment = shop_loot.generate_loot()
                        self.shop.show_items()
                        answer_to_buy = input(
                            "введите номер предмета для покупки(для выхода нажмите n): "
                        )
                        if answer_to_buy == "n":
                            break
                        self.shop.buy_item(self.current_player, answer_to_buy)

                    elif answer_shop == "2":
                        print(f"ваш инвентарь: {self.current_player.inventory}")
                        item_answer = input(
                            "введите порядковый номер предмета (начиная с 1): "
                        )
                        if item_answer.isdigit():
                            item_answer = int(item_answer)
                            if 1 <= item_answer <= len(self.current_player.inventory):
                                item_to_sell = self.current_player.inventory[
                                    item_answer - 1
                                ]  # Теперь тоже с 1!
                                self.shop.sell_item(self.current_player, item_to_sell)
                            else:
                                print("такого предмета в инвентаре нет")
                        else:
                            print("вы ввели не число, повторите ввод")

                    elif answer_shop == "3":
                        print(f"ваш инвентарь: {self.current_player.inventory}")
                        item_answer = input("введите порядковый номер предмета: ")
                        if item_answer.isdigit():
                            item_answer = int(item_answer)
                            if 1 <= item_answer <= len(self.current_player.inventory):
                                self.current_player.use_item(
                                    self.current_player.inventory[item_answer - 1]
                                )  # чтоб при пустом инвентаре не выходила ошибка
                                # if len(self.current_player.inventory) >= item_answer:
                                #     self.current_player.use_item(self.current_player.inventory[item_answer - 1])
                                break
                            else:
                                print("такого предмета в инвентаре нет")
                    else:
                        print("введено не правильное число")

                elif answer == "2":
                    break
                else:
                    print("введено не правильное число")

    def _process_player_action(self, enemy):
        """метод для обработки выбора игрока"""
        # if self.is_running:
        print(
            f"моя защита: {self.current_player.defense}, мое HP: {self.current_player.health}/{self.current_player.max_health}"
        )
        current_target = enemy
        print(f"Противник: {current_target.name} (HP: {current_target.health})")
        while True:
            answer = input(
                "что вы хотите сделать?"
                "\n1 - атаковать"
                "\n2 - использовать предмет"
                "\n3 - убежать"
            )

            if answer == "1":
                self.current_player.attack_target(current_target)
                if isinstance(self.current_player, Warrior):
                    self.current_player.buff_damage()
                if (
                    not current_target.is_alive()
                ):  # проверка на живучесть цели после удара
                    print(f"враг {current_target.name} мертв")
                    loot = enemy_loot[current_target.name].generate_loot()
                    for i in loot:
                        self.current_player.add_item(i)
                    self.current_player.gold += current_target.gold
                    print(
                        f"вы обыскали труп и нашли {current_target.gold} золота! всего золота: {self.current_player.gold}"
                    )
                    print(f"игрок {self.current_player.name} получил: {loot}")
                    # self.enemies.pop(0)
                    if isinstance(self.current_player, Warrior):
                        self.current_player.reset_damage()
                    self.start_shop_event()

                break

            elif answer == "2":
                print(f"ваш инвентарь: {self.current_player.inventory}")
                item_answer = input("введите порядковый номер предмета: ")
                if item_answer.isdigit():
                    item_answer = int(item_answer)
                    # Безопасная проверка: строго от 1 до размера инвентаря
                    if 1 <= item_answer <= len(self.current_player.inventory):
                        self.current_player.use_item(
                            self.current_player.inventory[item_answer - 1]
                        )
                        break
                    else:
                        print("такого предмета в инвентаре нет")
                else:
                    print("вы ввели не число, повторите ввод")

            elif answer == "3":
                return False

            else:
                print("введено не правильное число")

        return True

    def _process_enemy_turn(self, enemy):
        """Метод для автоматического хода противника"""
        # if self.is_running:
        attaker = enemy
        print(f"ход врага {attaker.name}")
        attaker.attack_target(self.current_player)
        # self.enemies.pop(0)

    def stop_game(self):
        answer = input("вы действительно хотите выйти? \nда\nнет: ")
        if answer == "да":
            self.is_running = False
        else:
            self.is_running = True


game = Game("подземелье колодца", "приключение в подземелье")
game.start_game()
