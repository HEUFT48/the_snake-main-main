from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
# Направления движения:
Pointer = tuple[int, int]
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

RGB = tuple[int, int, int]
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: RGB = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: RGB = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: RGB = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: RGB = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 3

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption(f'Змейка. Скорость змейки = {SPEED}')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс"""

    def __init__(
        self,
        position: Pointer = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
        body_color: RGB = BOARD_BACKGROUND_COLOR,
    ) -> None:
        self.position = position  
        self.body_color = body_color

    def draw(self):
        """Метода для отрисовки объекта на игровом поле"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, position: Pointer = CENTER, body_color: RGB = APPLE_COLOR, occupied_cells=None):
        super().__init__(position, body_color)
        self.randomize_position(occupied_cells or [])

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_cells):
        """Метод случайного положения яблока"""
        while True:
            self.position = (
                (randint(0, SCREEN_WIDTH) // GRID_SIZE) * GRID_SIZE,
                (randint(0, SCREEN_HEIGHT) // GRID_SIZE) * GRID_SIZE
            )
            if self.position not in occupied_cells:
                break


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self, position: Pointer = CENTER, body_color: RGB = SNAKE_COLOR):
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновление положения змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод изменения положения змеи"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_pos_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_pos_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_pos = (new_pos_x, new_pos_y)
        self.positions.insert(0, new_pos)
        self.last = (
            self.positions.pop() if len(self.positions) > self.length else None
        )
    

    def draw(self):
        """Метод отрисовки змеи"""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод управления с помощью клавиш"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змею в начальное состояние"""
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR


def handle_keys(game_object):
    """Управление при помощи клавы"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры"""
    pg.init()
    apple = Apple(body_color=APPLE_COLOR, position=CENTER)
    snake = Snake(body_color=SNAKE_COLOR, position=CENTER)
    while True:
        clock.tick(SPEED)
        apple.draw()
        pg.display.update()
        snake.draw()
        snake.move()
        snake.update_direction()
        handle_keys(snake)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

if __name__ == '__main__':
    main()
