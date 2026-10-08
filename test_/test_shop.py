from unittest.mock import patch

import pytest

from game import game_units
from game.exceptions import ItemNotFoundError, NotEnoughGoldError
from game.game_characters import Warrior
from game.game_units import Character
from game.Items import Consumable, Equipment, Item
from game.Shop import Shop

@pytest.fixture
def hero():
    return game_units.Unit(name="рыцарь", health=100, defense=10, attack=50)


