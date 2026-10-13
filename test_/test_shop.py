from Shop import Shop
import game_units
import pytest

from Items import Equipment
from exceptions import NotEnoughGoldError, ItemNotFoundError


@pytest.fixture
def hero():
    return game_units.Character(name="рыцарь", health=100, defense=10, attack=50)


def test_buy_item(hero):
    katana = Equipment(
        name="катана",
        description="острая катана",
        price=20,
        equipment_type="weapon",
        effect_value=20,
    )
    shop = Shop("магазин", [])
    shop.assortment.append(katana)
    shop.buy_item(hero, "0")

    assert hero.gold == 480
    assert hero.inventory == [katana]


def test_buy_item_not_enough_gold(hero):
    katana = Equipment(
        name="катана",
        description="острая катана",
        price=20,
        equipment_type="weapon",
        effect_value=20,
    )
    hero.gold = 10
    shop = Shop("магазин", [])
    shop.assortment.append(katana)
    with pytest.raises(NotEnoughGoldError):
        shop.buy_item(hero, "0")
    assert hero.gold == 10
    assert hero.inventory == []

def test_sell_item_success(hero):
    katana = Equipment(
        name="катана",
        description="острая катана",
        price=20,
        equipment_type="weapon",
        effect_value=20,
    )
    hero.inventory.append(katana)
    shop = Shop("магазин", [])
    shop.sell_item(hero, katana)
    assert hero.gold == 510
    assert hero.inventory == []
    assert shop.assortment == [katana]


def test_sell_item_not_in_inventory(hero):
    katana = Equipment(
        name="катана",
        description="острая катана",
        price=20,
        equipment_type="weapon",
        effect_value=20,
    )
    sword = Equipment(
        name="меч",
        description="простой меч",
        price=10,
        equipment_type="weapon",
        effect_value=10,
    )
    hero.inventory.append(katana)
    shop = Shop("магазин", [])
    with pytest.raises(ItemNotFoundError):
        shop.sell_item(hero, sword)
    assert hero.gold == 500
    assert shop.assortment == []