from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс."""

    def __init__(self, position=None, body_color=None):
        """Инициализация родительского класса."""
        self.body_color = body_color

        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position

    def draw(self):
        """Отрисовка объектов для переопределения в дочерних классах."""
        pass


class Apple(GameObject):
    """Дочерний класс 'Яблоко'."""

    def __init__(self, position=None, body_color=None):
        """Инициализация дочернего класса дял работы с объектом 'Яблоко'."""
        if body_color is None:
            body_color = APPLE_COLOR
        if position is None:
            position = self.randomize_position()
        super().__init__(position, body_color)

    @classmethod
    def randomize_position(cls):
        """Случайное размещение яблока на поле."""
        height_list = [
            square for square in range(SCREEN_HEIGHT) if square % GRID_SIZE == 0
        ]
        width_list = [
            square for square in range(SCREEN_WIDTH) if square % GRID_SIZE == 0
        ]
        height = choice(height_list)
        width = choice(width_list)
        return (width, height)

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс 'Змейка'."""

    def __init__(self, position=None, body_color=None):
        """Инициализация дочернего класса дял работы с объектом 'Змейка'."""
        if body_color is None:
            body_color = SNAKE_COLOR
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки"""
        self.update_direction()

        if self.positions:
            self.last = self.positions[-1]

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + GRID_SIZE * dx) % SCREEN_WIDTH
        new_y = (head_y + GRID_SIZE * dy) % SCREEN_HEIGHT
        new_position = (new_x, new_y)
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Определение позиции головы змейки"""
        if self.positions:
            return self.positions[0]
        else:
            return self.position

    def reset(self):
        """Сброс состояния змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработка клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная игра."""

    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple = Apple()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
