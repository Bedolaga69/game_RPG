import pytest

from game import game_units


@pytest.fixture
def hero():
    return game_units.Unit(name="рыцарь", health=100, defense=10, attack=50)

def test_get_damage(hero):
    hero.get_damage(50)
    assert hero.health == 40

def test_minimum_damage(hero):
    hero.get_damage(5)
    assert hero.health == 1

def test_maximum_damage(hero):
    hero.get_damage(500)
    assert hero.health == 0
    assert hero.is_alive() is False

def test_get_damage_fatal(hero):
    hero.get_damage(110)
    assert hero.health == 0