# Общая ошибка для всей игры
class GameError(Exception):
    pass

class UnknownEquipmentTypeError(GameError):
    pass

# Специфичные ошибки, которые наследуются от GameError
class NotEnoughGoldError(GameError):
    pass

class InventoryError(GameError):
    pass

class ItemNotFoundError(InventoryError):
    pass
