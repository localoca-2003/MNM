"""Trò chơi Rắn"""

import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 600      # Chiều rộng màn hình
SCREEN_HEIGHT = 480     # Chiều cao màn hình
SIZE = 20               # Kích thước ô vuông
LINE_WIDTH = 1          # Độ rộng đường lưới

# Phạm vi tọa độ của khu vực trò chơi
SCOPE_X = (0, SCREEN_WIDTH // SIZE - 1)
SCOPE_Y = (2, SCREEN_HEIGHT // SIZE - 1)

# Điểm số và màu sắc của thức ăn
FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]

LIGHT = (100, 100, 100)
DARK = (200, 200, 200)      # Màu của rắn
BLACK = (0, 0, 0)           # Màu đường lưới
RED = (200, 30, 30)         # Màu đỏ, màu chữ GAME OVER
BGCOLOR = (40, 40, 60)      # Màu nền


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


# Khởi tạo rắn
def init_snake():
    snake = deque()
    snake.append((2, SCOPE_Y[0]))
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))
    return snake


def create_food(snake):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        # Nếu thức ăn xuất hiện trên thân rắn, tạo lại
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return food_x, food_y


def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 2)]


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Trò Chơi Rắn')

    font1 = pygame.font.SysFont('SimHei', 24)  # Phông chữ hiển thị điểm
    font2 = pygame.font.Font(None, 72)  # Phông chữ GAME OVER
    fwidth, fheight = font2.size('GAME OVER')

    # Nếu rắn đang di chuyển sang phải, nhanh chóng nhấn xuống hoặc trái, do tốc độ làm mới của chương trình không đủ nhanh, điều này có thể dẫn đến việc rắn quay lại, gây GAME OVER
    # Biến b dùng để ngăn chặn tình huống này
    b = True

    # Rắn
    snake = init_snake()
    # Thức ăn
    food = create_food(snake)
    food_style = get_food_style()
    # Hướng di chuyển
    pos = (1, 0)

    game_over = True
    start = False       # Có bắt đầu hay không, khi start = True, game_over = True thì mới hiển thị GAME OVER
    score = 0           # Điểm số
    orispeed = 0.5      # Tốc độ ban đầu
    speed = orispeed
    last_move_time = None
    pause = False       # Tạm dừng

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        food = create_food(snake)
                        food_style = get_food_style()
                        pos = (1, 0)
                        # Điểm số
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    # Kiểm tra để tránh rắn di chuyển lên khi đã nhấn xuống, gây GAME OVER
                    if b and not pos[1]:
                        pos = (0, -1)
                        b = False
                elif event.key in (K_s, K_DOWN):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False
                elif event.key in (K_a, K_LEFT):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False
                elif event.key in (K_d, K_RIGHT):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False

        # Đổ màu nền
        screen.fill(BGCOLOR)
        # Vẽ đường lưới dọc
        for x in range(SIZE, SCREEN_WIDTH, SIZE):
            pygame.draw.line(screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
        # Vẽ đường lưới ngang
        for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:
                        # Ăn thức ăn
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = orispeed - 0.03 * (score // 100)
                        food = create_food(snake)
                        food_style = get_food_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        # Vẽ thức ăn
        if not game_over:
            # Tránh việc GAME OVER che khuất chữ GAME OVER
            pygame.draw.rect(screen, food_style[1], (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE), 0)

        # Vẽ rắn
        for s in snake:
            pygame.draw.rect(screen, DARK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                            SIZE - LINE_WIDTH * 2, SIZE - LINE_WIDTH * 2), 0)

        print_text(screen, font1, 30, 7, f'Toc do: {score//100}')
        print_text(screen, font1, 450, 7, f'Điem so: {score}')

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER', RED)

        pygame.display.update()


if __name__ == '__main__':
    main()

