import random

from game_units import *

class Warrior(Character):
    """Класс Воина с прогрессирующим уроном и повышенным здоровьем
    multiplier_damage - переменная для сохранения увеличенного урона для война и сбрасывающая его после убийства"""
    def __init__(self, name, equipped_weapon=None, equipped_armor=None):
        """инициализирует воина с базовыми характеристиками (HP: 250, Attack: 18, Defense: 10)"""
        super().__init__(name, 250, 18, 10, attack_speed = 80, equipped_weapon = equipped_weapon, equipped_armor = equipped_armor)
        self.multiplier_damage = 1.0

    def attack_target(self, other_character):
        """Атакует цель с учетом текущего множителя урона
        other_character
            персонаж-цель, принимающий урон"""
        actual_damage = self.attack * self.multiplier_damage#round - округление до 2 знаков после запятой
        print(f"урон повысился до {actual_damage}")
        print(f"{self.name} атакует {other_character.name}!")
        other_character.get_damage(actual_damage)

    def buff_damage(self):
        """метод для увеличения атаки после хода на 10%"""
        self.multiplier_damage += 0.1

    def reset_damage(self):
        """метод для сброса урона после убийства до базового значения"""
        self.multiplier_damage = 1.0
        print(f"урон у {self.name} сбросился до {self.attack}")

class Mage(Character):
    """Класс Мага с высоким базовым уроном и случайным разбросом силы заклинаний"""
    def __init__(self, name, equipped_weapon=None, equipped_armor=None):
        """инициализирует мага с базовыми характеристиками (HP: 150, Attack: 21, Defense: 5)"""
        super().__init__(name, 150, 21, 5, attack_speed = 110, equipped_weapon = equipped_weapon, equipped_armor = equipped_armor)

    def attack_target(self,other_character):
        """метод атаки цели с рандомным увеличением урона от атаки
        other_character
            персонаж-цель, принимающий урон"""
        actual_damage = random.randint(self.attack + 5, self.attack + 15)
        print(f"урон повысился до: {actual_damage}")
        print(f"{self.name} атакует {other_character.name}!")
        other_character.get_damage(actual_damage)

class Archer(Character):
    """Класс Лучника с высокой атакой и шансом критического попадания"""
    def __init__(self, name, equipped_weapon=None, equipped_armor=None):
        """инициализирует лучника с базовыми характеристиками (HP: 200, Attack: 30, Defense: 10)"""
        super().__init__(name, 200, 30, 10, attack_speed = 135,equipped_weapon = equipped_weapon, equipped_armor = equipped_armor)

    def attack_target(self,other_character):
        """метод атаки цели с шансом критического урона и увеличение урона при крит попадании вдвое
        other_character
            персонаж-цель, принимающий урон"""
        actual_damage = self.attack
        if random.randint(1, 5) == 3:
            actual_damage = self.attack * 2
            print("критический урон!")
        print(f"{self.name} атакует {other_character.name}!")
        other_character.get_damage(actual_damage)