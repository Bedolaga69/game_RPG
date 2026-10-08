import random

from exceptions import ItemNotFoundError, UnknownEquipmentTypeError
from Items import Consumable, Equipment
from status_effects import StatusEffect


class Unit:
    """класс базовых методов для создания всех сущностей"""

    def __init__(self, name, health, attack, defense, attack_speed=100):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.max_health = health
        self.attack_speed = attack_speed
        # Список для хранения объектов со статус эффектами
        self.active_effects = []

    def add_effect(self, name, duration, effect_value=0):
        """добавляет новый эффект или обновляет существующий"""
        for effect in self.active_effects:
            if effect.name == name:
                effect.duration = duration
                effect.effect_value = effect_value
                print(
                    f"эффект {name} на {self.name} обновлен! оставшиеся ходы {duration}"
                )
                return

        new_effect = StatusEffect(name, duration, effect_value)
        self.active_effects.append(new_effect)
        new_effect.on_apply(self)

    def update_effect(self):
        """применяет эффекты в начале раунда и удаляет истекшие эффекты"""
        expired_effects = []
        for effect in self.active_effects:
            effect.on_tick(self)

            if effect.duration <= 0:
                effect.on_remove(self)
                expired_effects.append(effect)

        for effect in expired_effects:
            self.active_effects.remove(effect)

    def get_damage(self, amount):
        """применяет входящий урон к юниту с учетом его защиты.

        Урон не может быть меньше 1, если здоровье падает до нуля или ниже,
        юнит считается поверженным
        amount
            количество входящего урона"""
        actual_damage = max(amount - self.defense, 1)
        if self.health <= actual_damage:
            self.health = 0
            print(f"{self.name} повержен!")
        else:
            self.health -= actual_damage
            print(
                f"{self.name} получает {actual_damage} урона, здоровье: {self.health}"
            )

    def attack_target(self, other_character):
        """метод для атаки цели с использованием метода нанесения урона
        other_character
            цель, которая примет урон"""
        print(f"{self.name} атакует {other_character.name}!")
        other_character.get_damage(self.attack)

    def is_alive(self):
        """проверка на жив ли противник/персонаж"""
        return self.health > 0


class Character(Unit):
    """класс управляемого персонажа игрока, обладающего инвентарем и экипировкой
    inventory - инвентарь тип: список
    gold - базовая голда
    equipped_weapon - надетое оружие
    equipped_armor - надетая броня
    base_defense - базовая защита
    base_attack - базовая атака
    defense - защита
    attack_speed - скорость атаки
    """

    def __init__(
        self,
        name,
        health,
        attack,
        defense,
        attack_speed=100,
        equipped_weapon=None,
        equipped_armor=None,
    ):
        """инициализирует персонажа игрока и автоматически рассчитывает бонусы от стартовой экипировки"""
        super().__init__(name, health, attack, defense, attack_speed)
        self.inventory = []
        self.gold = 500
        self.equipped_weapon = equipped_weapon
        self.equipped_armor = equipped_armor
        self.base_defense = defense
        self.base_attack = attack
        self.defense = self.base_defense
        if self.equipped_armor:
            self.defense += self.equipped_armor.effect_value
        self.attack = self.base_attack
        if self.equipped_weapon:
            self.attack += self.equipped_weapon.effect_value

    def reset_damage(self):
        """сбрасывает временные изменения урона для персонажа"""

    def use_item(self, item):
        if item not in self.inventory:
            raise ItemNotFoundError(f"предмета {item.name} нет в инвентаре")

        if isinstance(item, Equipment):
            self._equip(item)
        elif isinstance(item, Consumable):
            self._consume(item)

    def _equip(self, item):
        if item.equipment_type == "weapon":
            self.inventory.remove(item)
            if self.equipped_weapon is not None:
                self.attack -= self.equipped_weapon.effect_value
                self.inventory.append(self.equipped_weapon)
            self.equipped_weapon = item
            self.attack += item.effect_value
        elif item.equipment_type == "armor":
            self.inventory.remove(item)
            if self.equipped_armor is not None:
                self.defense -= self.equipped_armor.effect_value
                self.inventory.append(self.equipped_armor)
            self.equipped_armor = item
            self.defense += item.effect_value
        else:
            raise UnknownEquipmentTypeError(
                f"неизвестный тип экипировки у {item.name}: {item.equipment_type}"
            )
        print(f"вы экипировали {item.name}")

    def _consume(self, item):
        print(f"{self.name} использует {item}")
        if item.effect_type == "heal":
            self.health += item.effect_value
            self.health = min(self.max_health, self.health)
            print(f"текущее хп {self.name} = {self.health}")
        elif item.effect_type == "buff_defense":
            self.defense += item.effect_value
            print(f"текущая защита {self.name} = {self.defense}")
        elif item.effect_type == "buff_attack":
            self.attack += item.effect_value
            print(f"текущая атака {self.name} = {self.attack}")
        elif item.effect_type == "gold":
            max_gold_bonus = int(item.effect_value * 0.2)
            random_bonus = random.randint(-max_gold_bonus, max_gold_bonus)
            self.gold += item.effect_value + random_bonus
            print(f"вы получили {item.effect_value + random_bonus} золота с мешка")
        elif item.effect_type == "regeneration":
            self.add_effect("continuous_heal", item.duration, item.effect_value)
        elif item.effect_type == "poison":
            self.add_effect("poison", item.duration, item.effect_value)

        self.inventory.remove(item)

    def add_item(self, *items):
        """добавление предмета в инвентарь игроку
        item
            объект добавляемого предмета"""
        for item in items:
            self.inventory.append(item)
            print(f"{item.name} добавлен в инвентарь {self.name}")


class Enemy(Unit):
    """класс противника (монстра), с которого игрок может получить награду

    gold (int)
        количество золота, которое перейдет игроку после победы над врагом
    """

    def __init__(self, name, health, attack, defense, gold=0, attack_speed=100):
        super().__init__(name, health, attack, defense, attack_speed)
        self.gold = gold


armor = Equipment("броня", "дает 50 брони", "armor", 50, 250, 25)
mage_armor = Equipment("мантия", "дает 100 брони", "armor", 125, 150, 50)
leather_armor = Equipment("кожаные поножи", "дает 45 брони", "armor", 55, 45, 15)
