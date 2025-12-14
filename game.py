import sys
import pygame


pygame.init()


CELL_SIZE = 40
WALL_COLOR = (100, 100, 100)
EMPTY_COLOR = (230, 230, 230)
PLAYER_COLOR = (0, 120, 255)
COLLECTIBLE_COLOR = (255, 200, 0)
EXIT_COLOR = (0, 200, 100)
TEXT_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (255, 255, 255)


GAME_MAP = [
    "1111111111",
    "1P0C00E001",
    "1001001001",
    "1C0010C011",
    "1111100001",
    "1000000C01",
    "1011111101",
    "1C00000001",
    "1001C00E01",
    "1111111111"
]


player_pos = None
collectibles_count = 0

for y, row in enumerate(GAME_MAP):
    for x, cell in enumerate(row):
        if cell == 'P':
            player_pos = [x, y]
        elif cell == 'C':
            collectibles_count += 1

if player_pos is None:
    player_pos = [1, 1]


MAP_WIDTH = len(GAME_MAP[0])
MAP_HEIGHT = len(GAME_MAP)
WINDOW_WIDTH = MAP_WIDTH * CELL_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * CELL_SIZE


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Игра - Сбор предметов")
clock = pygame.time.Clock()


move_count = 0
collected_items = 0


font = pygame.font.SysFont(None, 24)


def draw_map():
    """Отрисовка карты."""
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)

            cell = GAME_MAP[y][x]

            if cell == '1':
                pygame.draw.rect(screen, WALL_COLOR, rect)
                pygame.draw.rect(screen, (70, 70, 70), rect, 2)
            elif cell == '0':
                pygame.draw.rect(screen, EMPTY_COLOR, rect)
                pygame.draw.rect(screen, (210, 210, 210), rect, 1)
            elif cell == 'C':
                pygame.draw.rect(screen, EMPTY_COLOR, rect)
                pygame.draw.rect(screen, (210, 210, 210), rect, 1)
                center_x = x * CELL_SIZE + CELL_SIZE // 2
                center_y = y * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, COLLECTIBLE_COLOR,
                                   (center_x, center_y), CELL_SIZE // 3)
            elif cell == 'E':
                pygame.draw.rect(screen, EXIT_COLOR, rect)
                pygame.draw.rect(screen, (0, 150, 80), rect, 3)
                text = font.render("E", True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(x * CELL_SIZE + CELL_SIZE // 2,
                            y * CELL_SIZE + CELL_SIZE // 2)
                )
                screen.blit(text, text_rect)


def draw_player():
    """Отрисовка игрока."""
    x, y = player_pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, rect)
    pygame.draw.rect(screen, (0, 80, 200), rect, 3)


def draw_info():
    """Отрисовка информации."""
    info_text = (f"Движений: {move_count}  |  "
                 f"Собрано: {collected_items}/{collectibles_count}")
    text_surface = font.render(info_text, True, TEXT_COLOR)
    screen.blit(text_surface, (10, 10))


def check_cell(x, y):
    """Проверка клетки карты."""
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return GAME_MAP[y][x]
    return '1'


def move_player(dx, dy):
    """Перемещение игрока."""
    global move_count, collected_items

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    target_cell = check_cell(new_x, new_y)

    if target_cell != '1':
        player_pos[0] = new_x
        player_pos[1] = new_y
        move_count += 1

        current_cell = GAME_MAP[new_y][new_x]
        if current_cell == 'C':
            row = list(GAME_MAP[new_y])
            row[new_x] = '0'
            GAME_MAP[new_y] = ''.join(row)
            collected_items += 1
            print(f"Предмет собран! Всего: {collected_items}/"
                  f"{collectibles_count}")

        elif current_cell == 'E':
            if collected_items == collectibles_count:
                print("Поздравляем! Вы прошли игру!")
                print(f"Всего движений: {move_count}")
                print(f"Собрано всех предметов: {collected_items}/"
                      f"{collectibles_count}")
                pygame.quit()
                sys.exit()
            else:
                remaining = collectibles_count - collected_items
                print(f"Нужно собрать все предметы! Осталось: {remaining}")

        print(f"Движений сделано: {move_count}")


def main():
    """Основной игровой цикл."""
    running = True

    print("2D Игра Сбор предметов ")
    print("Управление: W - вверх, S - вниз, A - влево, D - вправо")
    print("ESC - выход из игры")
    print(f"Цель: собрать все {collectibles_count} предмета и найти выход")
    print("=" * 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_w:
                    move_player(0, -1)
                elif event.key == pygame.K_s:
                    move_player(0, 1)
                elif event.key == pygame.K_a:
                    move_player(-1, 0)
                elif event.key == pygame.K_d:
                    move_player(1, 0)

        screen.fill(BACKGROUND_COLOR)
        draw_map()
        draw_player()
        draw_info()

        pygame.display.flip()
        clock.tick(60)

    print("\nИгра завершена!")
    print(f"Итоговое количество движений: {move_count}")
    print(f"Собрано предметов: {collected_items}/{collectibles_count}")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
