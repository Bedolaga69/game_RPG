import game_units
import pytest


@pytest.fixture
def hero():
    return game_units.Unit(name="рыцарь", health=100, defense=10, attack=50)
