"""Что обязательно нужно протестировать в use_item
Экипировка (Equipment):

Оружие и броня: Проверить, что старый предмет возвращается в inventory, новый записывается в equipped_weapon/equipped_armor, а attack/defense корректно пересчитываются.

Замена предмета: Снять старое оружие (уменьшив стат) и надеть новое (увеличив).

Неизвестный тип: Вызов UnknownEquipmentTypeError при item.equipment_type == "unknown".

Отсутствие в инвентаре: Вызов ItemNotFoundError.

Расходники (Consumable):

Лечение (heal): Проверить, что здоровье увеличивается, но не превышает max_health.

Баффы (buff_attack, buff_defense): Увеличение соответствующих характеристик.

Периодические эффекты (regeneration, poison): Вызов метода add_effect с нужными параметрами (effect_name, duration, value).

Золото (gold): Мешок золота содержит рандом (random.randint), поэтому для детерминированного теста стоит использовать unittest.mock.patch('random.randint').

Удаление: Предмет действительно исчезает из self.inventory после использования."""

from unittest.mock import patch

import pytest
from exceptions import ItemNotFoundError, UnknownEquipmentTypeError
from game_units import Character, Unit
from Items import Consumable, Equipment


@pytest.fixture
def hero():
    return Character("герой", 100, 25, 5)


def test_equip_weapon_success(hero):
    sword = Equipment(
        name="меч",
        description="простой меч",
        price=10,
        equipment_type="weapon",
        effect_value=10,
    )
    hero.inventory.append(sword)
    hero.use_item(sword)

    assert hero.equipped_weapon == sword
    assert hero.attack == 35
    assert sword not in hero.inventory


def test_swap_weapon(hero):
    sword = Equipment(
        name="меч",
        description="простой меч",
        price=10,
        equipment_type="weapon",
        effect_value=10,
    )
    katana = Equipment(
        name="катана",
        description="острая катана",
        price=20,
        equipment_type="weapon",
        effect_value=20,
    )
    hero.inventory.append(sword)
    hero.use_item(sword)
    assert hero.equipped_weapon == sword
    assert hero.attack == 35
    hero.inventory.append(katana)
    hero.use_item(katana)
    assert hero.equipped_weapon == katana
    assert hero.attack == 45


def test_equip_item_not_in_inventory_raises_error(hero):
    sword = Equipment(
        name="меч",
        description="простой меч",
        price=10,
        equipment_type="weapon",
        effect_value=10,
    )
    with pytest.raises(ItemNotFoundError):
        hero.use_item(sword)


def test_unknown_equipment_type_raises_error(hero):
    sword = Equipment(
        name="кольцо",
        description="магическое кольцо",
        price=15,
        equipment_type="ring",
        effect_value=10,
    )
    hero.inventory.append(sword)
    with pytest.raises(UnknownEquipmentTypeError):
        hero.use_item(sword)


def test_use_heal_potion_caps_at_max_health(hero):
    potion = Consumable(
        name="зелье",
        description="лечение",
        price=5,
        effect_type="heal",
        effect_value=50,
    )
    hero.inventory.append(potion)
    hero.health = 80
    hero.use_item(potion)
    assert hero.health == 100
    assert hero.inventory == []


def test_use_buff_attack_potion(hero):
    potion = Consumable(
        name="зелье",
        description="атака",
        price=5,
        effect_type="buff_attack",
        effect_value=10,
    )
    hero.inventory.append(potion)
    hero.attack = 25
    hero.use_item(potion)
    assert hero.attack == 35
    assert hero.inventory == []


def test_use_buff_defense_potion(hero):
    potion = Consumable(
        name="зелье",
        description="защита",
        price=5,
        effect_type="buff_defense",
        effect_value=10,
    )
    hero.inventory.append(potion)
    hero.defense = 10
    hero.use_item(potion)
    assert hero.defense == 20
    assert hero.inventory == []


@patch("random.randint", return_value=5)
def test_use_gold_bag(mock_randint, hero):
    potion = Consumable(
        name="мешок",
        description="золото",
        price=0,
        effect_type="gold",
        effect_value=100,
    )
    hero.gold = 50
    hero.inventory.append(potion)
    hero.use_item(potion)
    assert hero.gold == 155
    assert hero.inventory == []


@patch.object(Unit, "add_effect")
def test_use_regeneration_potion(mock_add_effect, hero):
    potion = Consumable(
        name="зелье регена",
        description="реген",
        price=10,
        effect_type="regeneration",
        effect_value=10,
        duration=3,
    )
    hero.inventory.append(potion)
    hero.use_item(potion)

    mock_add_effect.assert_called_once_with("continuous_heal", 3, 10)
    assert hero.inventory == []


@patch.object(Unit, "add_effect")
def test_use_poison_potion(mock_add_effect, hero):
    potion = Consumable(
        name="зелье яда",
        description="яд",
        price=10,
        effect_type="poison",
        effect_value=15,
        duration=3,
    )
    hero.inventory.append(potion)
    hero.use_item(potion)

    mock_add_effect.assert_called_once_with("poison", 3, 15)
    assert hero.inventory == []


# from unittest.mock import patch
#
# import pytest
# from exceptions import ItemNotFoundError, UnknownEquipmentTypeError
# from game_units import Character, Unit
# from Items import Consumable, Equipment
#
#
# @pytest.fixture
# def hero():
#     return Character("герой", 100, 25, 5)
#
# def test_equip_weapon_success(hero):
#     sword = Equipment(name="меч", equipment_type="weapon", effect_value=10)
#     hero.inventory.append(sword)
#     hero.use_item(sword)
#
#     assert hero.equipped_weapon == sword
#     assert hero.attack == 35
#     assert sword not in hero.inventory
#
#
# def test_swap_weapon(hero):
#     sword = Equipment(name="меч", equipment_type="weapon", effect_value=10)
#     katana = Equipment(name="катана", equipment_type="weapon", effect_value=20)
#     hero.inventory.append(sword)
#     hero.use_item(sword)
#     assert hero.equipped_weapon == sword
#     assert hero.attack == 35
#     hero.inventory.append(katana)
#     hero.use_item(katana)
#     assert hero.equipped_weapon == katana
#     assert hero.attack == 45
#
#
# def test_equip_item_not_in_inventory_raises_error(hero):
#     sword = Equipment(name="меч", equipment_type="weapon", effect_value=10)
#     with pytest.raises(ItemNotFoundError):
#         hero.use_item(sword)
#
#
# def test_unknown_equipment_type_raises_error(hero):
#     sword = Equipment(name="меч", equipment_type="ring", effect_value=10)
#     hero.inventory.append(sword)
#     with pytest.raises(UnknownEquipmentTypeError):
#         hero.use_item(sword)
#
#
# def test_use_heal_potion_caps_at_max_health(hero):
#     potion = Consumable(name="пидараска", effect_type="heal", effect_value=50)
#     hero.inventory.append(potion)
#     hero.health = 80
#     hero.use_item(potion)
#     assert hero.health == 100
#     assert hero.inventory == []
#
#
# def test_use_buff_attack_potion(hero):
#     potion = Consumable(name="пидараска", effect_type="buff_attack", effect_value=10)
#     hero.inventory.append(potion)
#     hero.attack = 25
#     hero.use_item(potion)
#     assert hero.attack == 35
#     assert hero.inventory == []
#
#
# def test_use_buff_defense_potion(hero):
#     potion = Consumable(name="пидараска", effect_type="buff_defense", effect_value=10)
#     hero.inventory.append(potion)
#     hero.defense = 10
#     hero.use_item(potion)
#     assert hero.defense == 20
#     assert hero.inventory == []
#
#
# @patch("random.randint", return_value=5)  # Заставляем random.randint всегда возвращать 5
# def test_use_gold_bag(mock_randint, hero):
#     potion = Consumable(name="мешок", effect_type="gold", effect_value=100)
#     hero.gold = 50
#     hero.inventory.append(potion)
#     hero.use_item(potion)
#     assert hero.gold == 155
#     assert hero.inventory == []
#
#
# @patch.object(Unit, "add_effect")
# def test_use_regeneration_potion(mock_add_effect, hero):
#     potion = Consumable(
#         name="зелье регена", effect_type="regeneration", effect_value=10, duration=3
#     )
#     hero.inventory.append(potion)
#     hero.use_item(potion)
#
#     mock_add_effect.assert_called_once_with("continuous_heal", 3, 10)
#     assert hero.inventory == []
#
#
# @patch.object(Unit, "add_effect")
# def test_use_poison_potion(mock_add_effect, hero):
#     potion = Consumable(name="зелье яда", effect_type="poison", effect_value=15, duration=3)
#     hero.inventory.append(potion)
#     hero.use_item(potion)
#
#     mock_add_effect.assert_called_once_with("poison", 3, 15)
#     assert hero.inventory == []
