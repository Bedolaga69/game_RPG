import game_characters
import pytest
from item_storage import ITEMS, LootTable


def test_generate_loot(monkeypatch):
    loot = LootTable()
    loot.add_drop("sword", 0.5)
    loot.add_drop("armor", 0.05)
    monkeypatch.setattr("random.random", lambda: 0.1)
    result = loot.generate_loot()
    assert ITEMS["sword"] in result
    assert ITEMS["armor"] not in result


@pytest.fixture
def hero():
    return game_characters.Warrior(
        name="Воин", equipped_weapon=None, equipped_armor=None
    )


def test_warrior(hero):
    hero.multiplier_damage = 1.0

    hero.buff_damage()
    assert hero.multiplier_damage == pytest.approx(1.1)
    hero.reset_damage()
    assert hero.multiplier_damage == 1.0
