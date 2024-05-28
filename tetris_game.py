import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

COLORS = [BLACK, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE, PURPLE]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1],
    [0, 1, 0]],  # T
    [[1, 1],
    [1, 1]],  # O
    [[0, 1, 1],
    [1, 1, 0]],  # Z
    [[1, 1, 0],
    [0, 1, 1]],  # S
    [[1, 1, 1],
    [1, 0, 0]],  # L
    [[1, 1, 1],
    [0, 0, 1]]  # J
]

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Tetrimino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def image(self):
        rotated_shape = self.shape
        for _ in range(self.rotation):
            rotated_shape = rotate_shape(rotated_shape)
        return rotated_shape

    def rotate(self):
        original_rotation = self.rotation
        self.rotation = (self.rotation + 1) % 4  # Ensure four possible rotations
        if not valid_space(self, create_grid()):
            self.rotation = original_rotation  # Revert rotation if it's not valid

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(GRID_WIDTH) if grid[y][x] == BLACK] for y in range(GRID_HEIGHT)]
    accepted_positions = [x for sub in accepted_positions for x in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def convert_shape_format(shape):
    positions = []
    format = shape.image()

    # Debug print statements
    print(f"Shape: {shape.shape}")
    print(f"Rotation: {shape.rotation}")
    print(f"Format: {format}")

    # Ensure format is a list of lists
    if not isinstance(format, list) or not all(isinstance(row, list) for row in format):
        raise ValueError(f"Shape format is not a list of lists: {format}")

    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == 1:
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])
    return positions

def clear_rows(grid, locked):
    increment = 0
    rows_to_clear = []

    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            rows_to_clear.append(i)
            increment += 1

    if rows_to_clear:
        print(f"Rows to clear: {rows_to_clear}")

    for row in rows_to_clear:
        for j in range(len(grid[row])):
            try:
                del locked[(j, row)]
            except KeyError:
                continue

    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < min(rows_to_clear):
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment



def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (SCREEN_WIDTH / 2 - (label.get_width() / 2), SCREEN_HEIGHT / 2 - (label.get_height() / 2)))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    draw_grid_lines(surface, grid)

def draw_grid_lines(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, WHITE, (0, i * GRID_SIZE), (SCREEN_WIDTH, i * GRID_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, WHITE, (j * GRID_SIZE, 0), (j * GRID_SIZE, SCREEN_HEIGHT))

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    draw_text_middle(f'Score: {score}', 30, WHITE, surface)
