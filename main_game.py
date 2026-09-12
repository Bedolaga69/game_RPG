import pygame
import sys
import random
import os

from game_characters import Warrior, Mage, Archer
from game_units import Enemy
from Shop import Shop
from item_storage import ITEMS, shop_loot, enemy_loot, LootTable

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Подземелье — Ultimate Edition")
clock = pygame.time.Clock()

FONT_LARGE = pygame.font.SysFont("Arial", 36, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 20, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 16)


def load_image(filename, size, fallback_color):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(img, size)
    else:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2)
        return surf


IMAGES = {
    "bg_battle": load_image("images/bg_battle.jpg", (WIDTH, HEIGHT), (40, 40, 50)),
    "bg_shop": load_image("images/bg_shop.jpg", (WIDTH, HEIGHT), (60, 40, 30)),
    "bg_inventory": load_image("images/bg_inventory.jpg", (WIDTH, HEIGHT), (30, 50, 40)),
    "bg_death": load_image("images/bg_death.jpg", (WIDTH, HEIGHT), (100, 20, 20)),

    "hero_warrior": load_image("images/warrior.png", (120, 150), (50, 150, 255)),
    "hero_mage": load_image("images/mage.png", (120, 150), (150, 50, 255)),
    "hero_archer": load_image("images/archer.png", (120, 150), (50, 255, 100)),
    "enemy_goblin": load_image("images/goblin.png", (120, 150), (100, 255, 100)),
    "enemy_skeleton": load_image("images/skeleton.png", (120, 150), (200, 200, 200)),
    "enemy_orc": load_image("images/orc.png", (140, 170), (50, 150, 50)),
    "enemy_vampire": load_image("images/vampire.png", (120, 150), (200, 50, 50)),
    "enemy_golem": load_image("images/golem.png", (160, 190), (100, 100, 100)),
    "enemy_lich": load_image("images/lich.png", (130, 160), (50, 200, 200)),
    "enemy_dark_seeker": load_image("images/dark_seeker.png", (120, 150), (50, 50, 50)),
    "item_sword": load_image("images/sword.png", (64, 64), (200, 200, 200)),
    "item_armor": load_image("images/armor.png", (64, 64), (100, 100, 200)),
    "item_potion_heal": load_image("images/potion_heal.png", (64, 64), (255, 50, 50)),
    "item_potion_buff": load_image("images/potion_buff.png", (64, 64), (50, 50, 255)),
    "item_gold": load_image("images/gold.png", (64, 64), (255, 215, 0)),
    "item_default": load_image("images/item_default.png", (64, 64), (150, 150, 150))
}


def get_enemy_image(enemy_name):
    mapping = {
        "Гоблин": "enemy_goblin", "Скелет": "enemy_skeleton",
        "Орк": "enemy_orc", "Темный Искатель": "enemy_dark_seeker",
        "Каменный Голем": "enemy_golem", "Вампир": "enemy_vampire",
        "Древний Лич": "enemy_lich"
    }
    return mapping.get(enemy_name, "enemy_goblin")


def get_item_image(item):
    name = item.name.lower()
    if "меч" in name or "экскалибур" in name or "скорбь" in name: return "item_sword"
    if "брон" in name or "нагрудник" in name or "кираса" in name or "поножи" in name: return "item_armor"
    if "здоровь" in name or "реген" in name or "фласка" in name: return "item_potion_heal"
    if "зелье" in name: return "item_potion_buff"
    if "мешок" in name or "золот" in name: return "item_gold"
    return "item_default"


class FloatingText:
    def __init__(self, x, y, text, color):
        self.x, self.y, self.text, self.color, self.timer = x, y, text, color, 45

    def update(self):
        self.y -= 2
        self.timer -= 1

    def draw(self, surface):
        if self.timer > 0:
            surface.blit(FONT_LARGE.render(self.text, True, self.color), (self.x, self.y))


class VisualSprite:
    def __init__(self, x, y, image_key, is_enemy=False):
        self.start_x, self.start_y = x, y
        self.x, self.y = x, y
        self.image_key = image_key
        self.is_enemy = is_enemy
        self.anim_timer = 0

    def trigger_attack(self):
        self.anim_timer = 20

    def update(self):
        if self.anim_timer > 0:
            self.anim_timer -= 1
            direction = -1 if self.is_enemy else 1
            if self.anim_timer > 10:
                self.x += 15 * direction
            else:
                self.x -= 15 * direction
            if self.anim_timer <= 0:
                self.x = self.start_x

    def draw(self, surface, offset_x, offset_y):
        surface.blit(IMAGES[self.image_key], (self.x + offset_x, self.y + offset_y))


class PygameRPG:
    def __init__(self):
        self.state = "CHAR_SELECT"
        self.player, self.enemies = None, []
        self.current_enemy_idx = 0
        self.shop = Shop("магазинчик", [])
        self.shop_mode = "BUY"
        self.player_sprite = None
        self.enemy_sprite = None

        self.floating_texts = []
        self.screen_shake = 0
        self.enemy_templates = [
            ("Гоблин", 28, 15, 4, 15), ("Скелет", 50, 20, 5, 25),
            ("Орк", 100, 30, 13, 50), ("Темный Искатель", 65, 41, 6, 35),
            ("Каменный Голем", 150, 20, 20, 60), ("Вампир", 110, 23, 10, 90),
            ("Древний Лич", 200, 50, 15, 300)
        ]

    def select_character(self, char_class, sprite_key):
        self.player = char_class(name="Игрок")
        # Даем базовые зелья на старте
        if "heal_potion" in ITEMS and "regen_potion" in ITEMS:
            self.player.add_item(ITEMS["heal_potion"], ITEMS["regen_potion"])
        self.player_sprite = VisualSprite(150, 350, sprite_key, False)

        for i in range(10):
            tmpl = self.enemy_templates[i % len(self.enemy_templates)]
            self.enemies.append(Enemy(tmpl[0], tmpl[1], tmpl[2], tmpl[3], tmpl[4]))

        self.spawn_enemy()
        self.state = "BATTLE"

    def spawn_enemy(self):
        enemy = self.current_enemy()
        if enemy:
            self.enemy_sprite = VisualSprite(600, 350, get_enemy_image(enemy.name), True)

    def current_enemy(self):
        return self.enemies[self.current_enemy_idx] if self.current_enemy_idx < len(self.enemies) else None

    def add_floating_text(self, x, y, amount, color):
        self.floating_texts.append(FloatingText(x, y, str(amount), color))

    def attempt_run(self):
        rndm = random.randint(0, 3)
        if rndm == 2:
            self.state = "RUN_SUCCESS"
        else:
            self.add_floating_text(400, 300, "НЕУДАЧА!", (255, 0, 0))
            self.enemy_sprite.trigger_attack()
            enemy = self.current_enemy()
            if enemy:
                dmg = max(enemy.attack - self.player.defense, 1)
                self.player.health -= dmg
            self.screen_shake = 15
            if not self.player.is_alive():
                self.state = "GAME_OVER"

    def process_turn_end(self):
        if self.player and hasattr(self.player, 'update_effect'):
            self.player.update_effect()
        enemy = self.current_enemy()
        if enemy and hasattr(enemy, 'update_effect'):
            enemy.update_effect()

    def player_attack(self):
        enemy = self.current_enemy()
        if not enemy or self.player_sprite.anim_timer > 0 or self.enemy_sprite.anim_timer > 0:
            return

        if isinstance(self.player, Warrior) and hasattr(self.player, 'buff_damage'):
            self.player.buff_damage()

        multiplier = getattr(self.player, 'multiplier_damage', 1.0)
        dmg = max(self.player.attack * multiplier - enemy.defense, 1)

        if hasattr(self.player, 'attack_target'):
            self.player.attack_target(enemy)
        else:
            enemy.health -= dmg

        self.player_sprite.trigger_attack()
        self.add_floating_text(self.enemy_sprite.x + 50, self.enemy_sprite.y - 20, f"-{int(dmg)}", (255, 50, 50))
        self.screen_shake = 10

        if not enemy.is_alive():
            if isinstance(self.player, Warrior) and hasattr(self.player, 'reset_damage'):
                self.player.reset_damage()

            loot_table = enemy_loot.get(enemy.name, LootTable())
            earned_loot = loot_table.generate_loot()
            if earned_loot:
                for itm in earned_loot:
                    self.player.add_item(itm)

            self.player.gold += enemy.gold
            self.add_floating_text(400, 250, f"+{enemy.gold} Золота!", (255, 215, 0))

            self.current_enemy_idx += 1
            if self.current_enemy_idx >= len(self.enemies):
                self.state = "VICTORY"
            else:
                if random.random() < 0.5:
                    self.shop.assortment = shop_loot.generate_loot()
                    self.state = "SHOP_PROMPT"
                else:
                    self.spawn_enemy()
        else:
            enemy_dmg = max(enemy.attack - self.player.defense, 1)
            if hasattr(enemy, 'attack_target'):
                enemy.attack_target(self.player)
            else:
                self.player.health -= enemy_dmg

            self.enemy_sprite.trigger_attack()
            self.add_floating_text(self.player_sprite.x + 50, self.player_sprite.y - 20, f"-{enemy_dmg}", (255, 50, 50))
            self.screen_shake = 15

            self.process_turn_end()

            if not self.player.is_alive():
                self.state = "GAME_OVER"

    def draw_health_bar(self, x, y, hp, max_hp, name):
        pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, 254, 24))
        pygame.draw.rect(screen, (100, 30, 30), (x, y, 250, 20))
        pygame.draw.rect(screen, (50, 200, 50), (x, y, 250 * max(0, hp / max_hp), 20))
        screen.blit(FONT_MED.render(f"{name} {int(hp)}/{max_hp}", True, (255, 255, 255)), (x, y - 25))

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
            shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
            if self.screen_shake > 0:
                self.screen_shake -= 1

            if self.state == "CHAR_SELECT":
                screen.fill((30, 30, 40))
                screen.blit(FONT_LARGE.render("ВЫБЕРИТЕ КЛАСС", True, (255, 255, 255)), (300, 100))
                btn_w = pygame.Rect(150, 250, 150, 200)
                btn_m = pygame.Rect(375, 250, 150, 200)
                btn_a = pygame.Rect(600, 250, 150, 200)

                for btn, img, txt, cls, key in [
                    (btn_w, "hero_warrior", "Воин", Warrior, "hero_warrior"),
                    (btn_m, "hero_mage", "Маг", Mage, "hero_mage"),
                    (btn_a, "hero_archer", "Лучник", Archer, "hero_archer")]:
                    pygame.draw.rect(screen, (60, 60, 80) if btn.collidepoint(mouse_pos) else (40, 40, 60), btn,
                                     border_radius=10)
                    screen.blit(IMAGES[img], (btn.x + 15, btn.y + 10))
                    screen.blit(FONT_MED.render(txt, True, (255, 255, 255)), (btn.x + 40, btn.y + 170))

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if btn_w.collidepoint(mouse_pos):
                            self.select_character(Warrior, "hero_warrior")
                        elif btn_m.collidepoint(mouse_pos):
                            self.select_character(Mage, "hero_mage")
                        elif btn_a.collidepoint(mouse_pos):
                            self.select_character(Archer, "hero_archer")

            elif self.state == "SHOP_PROMPT":
                screen.blit(IMAGES["bg_battle"], (0, 0))
                s = pygame.Surface((WIDTH, HEIGHT))
                s.set_alpha(200)
                s.fill((0, 0, 0))
                screen.blit(s, (0, 0))
                screen.blit(FONT_LARGE.render("Впереди виднеется лавка торговца.", True, (255, 255, 255)), (180, 200))
                screen.blit(FONT_LARGE.render("Зайти внутрь?", True, (255, 215, 0)), (320, 250))

                btn_yes = pygame.Rect(300, 350, 120, 50)
                btn_no = pygame.Rect(450, 350, 120, 50)
                pygame.draw.rect(screen, (50, 150, 50) if btn_yes.collidepoint(mouse_pos) else (30, 100, 30), btn_yes,
                                 border_radius=10)
                screen.blit(FONT_MED.render("Да", True, (255, 255, 255)), (btn_yes.x + 45, btn_yes.y + 12))
                pygame.draw.rect(screen, (150, 50, 50) if btn_no.collidepoint(mouse_pos) else (100, 30, 30), btn_no,
                                 border_radius=10)
                screen.blit(FONT_MED.render("Нет", True, (255, 255, 255)), (btn_no.x + 40, btn_no.y + 12))

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if btn_yes.collidepoint(mouse_pos):
                            self.state = "SHOP"
                            self.shop_mode = "BUY"
                        elif btn_no.collidepoint(mouse_pos):
                            self.state = "BATTLE"
                            self.spawn_enemy()

            elif self.state == "BATTLE":
                screen.blit(IMAGES["bg_battle"], (shake_x, shake_y))
                self.player_sprite.update()
                self.player_sprite.draw(screen, shake_x, shake_y)
                enemy = self.current_enemy()

                if enemy:
                    self.enemy_sprite.update()
                    self.enemy_sprite.draw(screen, shake_x, shake_y)
                    self.draw_health_bar(600, 50, enemy.health, enemy.max_health, enemy.name)
                self.draw_health_bar(50, 50, self.player.health, self.player.max_health, self.player.name)

                for ft in self.floating_texts[:]:
                    ft.update()
                    ft.draw(screen)
                    if ft.timer <= 0:
                        self.floating_texts.remove(ft)

                pygame.draw.rect(screen, (30, 30, 35), (0, 500, WIDTH, 150))
                btn_atk = pygame.Rect(50, 520, 200, 50)
                btn_inv = pygame.Rect(270, 520, 200, 50)
                btn_run = pygame.Rect(490, 520, 200, 50)

                for btn, txt, clr, hover in [
                    (btn_atk, "Атака", (100, 30, 30), (150, 50, 50)),
                    (btn_inv, "Рюкзак", (30, 100, 30), (50, 150, 50)),
                    (btn_run, "Убежать", (30, 30, 100), (50, 50, 150))]:
                    pygame.draw.rect(screen, hover if btn.collidepoint(mouse_pos) else clr, btn, border_radius=10)
                    screen.blit(FONT_MED.render(txt, True, (255, 255, 255)), (btn.x + 30, btn.y + 12))

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if btn_atk.collidepoint(mouse_pos):
                            self.player_attack()
                        elif btn_inv.collidepoint(mouse_pos):
                            self.state = "INVENTORY"
                        elif btn_run.collidepoint(mouse_pos):
                            self.attempt_run()

            elif self.state in ["SHOP", "INVENTORY"]:
                screen.blit(IMAGES["bg_shop" if self.state == "SHOP" else "bg_inventory"], (0, 0))
                title = "ЛАВКА ТОРГОВЦА" if self.state == "SHOP" else "ВАШ РЮКЗАК"
                screen.blit(FONT_LARGE.render(title, True, (255, 215, 0)), (50, 20))
                screen.blit(FONT_MED.render(f"Золото: {self.player.gold}", True, (255, 255, 255)), (50, 70))

                btn_mode_buy = None
                btn_mode_sell = None
                if self.state == "SHOP":
                    btn_mode_buy = pygame.Rect(300, 60, 100, 35)
                    btn_mode_sell = pygame.Rect(410, 60, 100, 35)
                    pygame.draw.rect(screen, (50, 150, 50) if self.shop_mode == "BUY" else (40, 40, 60), btn_mode_buy,
                                     border_radius=5)
                    pygame.draw.rect(screen, (50, 150, 50) if self.shop_mode == "SELL" else (40, 40, 60), btn_mode_sell,
                                     border_radius=5)
                    screen.blit(FONT_SMALL.render("Купить", True, (255, 255, 255)),
                                (btn_mode_buy.x + 25, btn_mode_buy.y + 8))
                    screen.blit(FONT_SMALL.render("Продать", True, (255, 255, 255)),
                                (btn_mode_sell.x + 20, btn_mode_sell.y + 8))

                if self.state == "SHOP":
                    items_list = self.shop.assortment if self.shop_mode == "BUY" else self.player.inventory
                else:
                    items_list = self.player.inventory

                hovered_item = None
                hovered_index = -1
                hovered_rect = None

                for i, item in enumerate(items_list):
                    x, y = 100 + (i % 5) * 100, 150 + (i // 5) * 100
                    item_rect = pygame.Rect(x, y, 64, 64)
                    screen.blit(IMAGES[get_item_image(item)], (x, y))
                    if item_rect.collidepoint(mouse_pos):
                        hovered_item = item
                        hovered_index = i
                        hovered_rect = item_rect

                if hovered_item:
                    pygame.draw.rect(screen, (255, 255, 255), hovered_rect, 3)
                    tooltip = pygame.Rect(mouse_pos[0] + 15, mouse_pos[1] + 15, 340, 85)
                    if tooltip.right > WIDTH: tooltip.x = WIDTH - tooltip.width - 5
                    if tooltip.bottom > HEIGHT: tooltip.y = HEIGHT - tooltip.height - 5

                    pygame.draw.rect(screen, (20, 20, 30), tooltip, border_radius=5)
                    pygame.draw.rect(screen, (200, 200, 200), tooltip, 2, border_radius=5)

                    price_text = f"{hovered_item.price}g" if (
                                self.state != "SHOP" or self.shop_mode == "BUY") else f"Продажа: {hovered_item.price // 2}g"
                    screen.blit(FONT_MED.render(f"{hovered_item.name} ({price_text})", True, (255, 215, 0)),
                                (tooltip.x + 10, tooltip.y + 5))
                    screen.blit(FONT_SMALL.render(hovered_item.description, True, (200, 200, 200)),
                                (tooltip.x + 10, tooltip.y + 35))

                    if self.state == "SHOP":
                        action_text = "Клик - купить" if self.shop_mode == "BUY" else "Клик - продать за полцены"
                    else:
                        action_text = "Клик - экипировать/использовать"
                    screen.blit(FONT_SMALL.render(action_text, True, (100, 255, 100)), (tooltip.x + 10, tooltip.y + 55))

                btn_close = pygame.Rect(700, 50, 150, 50)
                pygame.draw.rect(screen, (200, 50, 50), btn_close, border_radius=10)
                screen.blit(FONT_MED.render("Закрыть", True, (255, 255, 255)), (730, 62))

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if btn_close.collidepoint(mouse_pos):
                            if self.state == "SHOP":
                                self.state = "BATTLE"
                                self.spawn_enemy()
                            else:
                                self.state = "BATTLE"
                        elif self.state == "SHOP" and btn_mode_buy and btn_mode_buy.collidepoint(mouse_pos):
                            self.shop_mode = "BUY"
                        elif self.state == "SHOP" and btn_mode_sell and btn_mode_sell.collidepoint(mouse_pos):
                            self.shop_mode = "SELL"
                        elif hovered_item and hovered_rect.collidepoint(mouse_pos):
                            if self.state == "SHOP":
                                if self.shop_mode == "BUY":
                                    gold_before = self.player.gold
                                    self.shop.buy_item(self.player, str(hovered_index))
                                    if self.player.gold < gold_before:
                                        self.shop.assortment.pop(hovered_index)
                                else:
                                    self.shop.sell_item(self.player, hovered_item)
                            else:
                                self.player.use_item(hovered_item)
                                if hovered_item in self.player.inventory:
                                    self.player.inventory.remove(hovered_item)

            elif self.state == "GAME_OVER":
                screen.fill((50, 0, 0))
                screen.blit(FONT_LARGE.render("вы мертвы...", True, (255, 255, 255)),
                            (WIDTH // 2 - 115, HEIGHT // 2))

            elif self.state == "RUN_SUCCESS":
                screen.fill((0, 50, 100))
                screen.blit(FONT_LARGE.render("вам удалось сбежать!", True, (255, 255, 255)),
                            (WIDTH // 2 - 220, HEIGHT // 2))

            elif self.state == "VICTORY":
                screen.fill((0, 50, 0))
                screen.blit(FONT_LARGE.render("победа!! вы прошли подземелье!!", True, (255, 215, 0)),
                            (WIDTH // 2 - 320, HEIGHT // 2))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PygameRPG()
    game.run()