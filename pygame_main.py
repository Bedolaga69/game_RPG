import pygame
import sys
# Импортируем твои классы из твоих файлов
from game_characters import Warrior
from game_units import Enemy

# Инициализация PyGame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Подземелье - Асиятилов Рамзес Магомедович")

# Шрифты и цвета
font = pygame.font.SysFont("Arial", 26, bold=True)
small_font = pygame.font.SysFont("Arial", 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)

# Инициализация игровых объектов (используем твою логику)
# Создаем Воина с базовыми характеристиками из твоего кода
player = Warrior(name="Герой")
# Создаем Гоблина со статами из твоего метода _create_default_enemies
enemy = Enemy("Гоблин", 28, 15, 4, 15)

# Переменная для вывода логов на экран
battle_log = "Бой начался!"


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        text_img = font.render(self.text, True, BLACK)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Создаем кнопки интерфейса (замена твоему input[span_3](start_span)[span_3](end_span))
btn_attack = Button(50, 500, 150, 50, "Атака")
btn_heal = Button(220, 500, 150, 50, "Предмет")
btn_run = Button(390, 500, 150, 50, "Убежать")


def draw_health_bar(surface, x, y, hp, max_hp, name):
    pygame.draw.rect(surface, RED, (x, y, 200, 20))
    if hp > 0:
        ratio = hp / max_hp
        pygame.draw.rect(surface, GREEN, (x, y, 200 * ratio, 20))
    pygame.draw.rect(surface, WHITE, (x, y, 200, 20), 2)

    text = small_font.render(f"{name}: {hp}/{max_hp}", True, WHITE)
    surface.blit(text, (x, y - 25))


# --- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ PYGAME ---
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(DARK_GRAY)

    # 1. Обработка событий (клики, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Логика нажатия на кнопку "Атака"
            if btn_attack.is_clicked(mouse_pos) and player.is_alive() and enemy.is_alive():
                # Вызываем твой метод атаки по цели[span_4](start_span)[span_4](end_span)
                player.attack_target(enemy)
                player.buff_damage()
                battle_log = f"Вы атаковали {enemy.name}!"

                # Если враг выжил, он атакует в ответ (как в твоем _process_enemy_turn[span_5](start_span)[span_5](end_span))
                if enemy.is_alive():
                    enemy.attack_target(player)
                    battle_log += f" Враг нанес ответный удар!"
                else:
                    battle_log = f"Враг {enemy.name} повержен! Золото: +{enemy.gold}"
                    player.gold += enemy.gold
                    player.reset_damage()

            elif btn_heal.is_clicked(mouse_pos):
                battle_log = "Функция использования предметов в разработке..."

            elif btn_run.is_clicked(mouse_pos):
                battle_log = "Вы сбежали из боя!"
                enemy.health = 0  # Техническое завершение боя для примера

    # 2. Отрисовка интерфейса
    draw_health_bar(screen, 50, 100, player.health, player.max_health, player.name)
    draw_health_bar(screen, 550, 100, enemy.health, enemy.max_health, enemy.name)

    # Отрисовка кнопок
    btn_attack.draw(screen)
    btn_heal.draw(screen)
    btn_run.draw(screen)

    # Отрисовка текста логов боя
    log_text = small_font.render(battle_log, True, WHITE)
    screen.blit(log_text, (50, 400))

    if not player.is_alive():
        game_over = font.render("ВЫ ПОГИБЛИ", True, RED)
        screen.blit(game_over, (WIDTH // 2 - 100, HEIGHT // 2))

    if not enemy.is_alive() and player.is_alive():
        win_text = font.render("ПОБЕДА!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 60, HEIGHT // 2))

    # 3. Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()