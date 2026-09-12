## shop

 - [show_items()](Shop.py) — показывает все вещи которые есть в магазине с их ценой
 - [buy_item()](Shop.py) — покупка предмета по индексу и вывод баланса персонажа
 - [sell_item()](Shop.py) — продажа предмета за половину его цены
 
## game

 - [start_game()](game.py) — старт игры с выбором персонажа
 - [_create_default_enemies()](game.py) — приватный метод для создания набора врагов
 - [_start_battle_loop()](game.py) — начало игрового лупа
 - [start_shop_event()](game.py) — открытие магазина для покупки предметов со своим шансом в магазине
 - [_process_player_action()](game.py) — метод для обработки выбора игрока
 - [_process_enemy_turn()](game.py) — метод для автоматического хода противника
 - [stop_game()](game.py) — метод для завершения игры

## game_characters

 - [attack_target()](game_characters.py) — атака цели с учетом особенностей класса персонажа (воин, маг, лучник)
 - [buff_damage()](game_characters.py) — метод для увеличения атаки воина после хода на 10%
 - [reset_damage()](game_characters.py) — метод для сброса урона воина после убийства до базового значения

## game_units

 - [get_damage()](game_units.py) — применяется входящий урон к юниту с учетом его защиты
 - [attack_target()](game_units.py) — метод для атаки цели с использованием метода нанесения урона
 - [is_alive()](game_units.py) — проверка на жив ли противник или персонаж
 - [use_item()](game_units.py) — использует предмет из инвентаря персонажа
 - [add_item()](game_units.py) — добавление предмета в инвентарь игроку

## item_storage

 - [add_drop()](item_storage.py) — метод для добавления предметов в пул дропа по индексу
 - [generate_loot()](item_storage.py) — метод для генерации лута через независимые броски кубика