import pygame

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.create_grid()

    def create_grid(self):
        return [[(0, 0, 0) for _ in range(self.cols)] for _ in range(self.rows)]

    def update(self, locked_positions):
        self.grid = self.create_grid()
        for pos in locked_positions:
            x, y = pos
            self.grid[y][x] = locked_positions[pos]

    def draw(self, surface, top_left_x, top_left_y, play_width, play_height, block_size):
        for i in range(self.rows):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size),
                             (top_left_x + play_width, top_left_y + i * block_size))
            for j in range(self.cols):
                pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * block_size, top_left_y),
                                 (top_left_x + j * block_size, top_left_y + play_height))
