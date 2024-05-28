import pygame

class Display:
    def __init__(self, top_left_x, top_left_y, play_width, play_height, block_size):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.play_width = play_width
        self.play_height = play_height
        self.block_size = block_size

    def draw_text_middle(self, text, size, color, surface):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        surface.blit(label, (self.top_left_x + self.play_width / 2 - (label.get_width() / 2),
                             self.top_left_y + self.play_height / 2 - (label.get_height() / 2)))

    def draw_window(self, surface, grid, next_piece, score):
        surface.fill((0, 0, 0))
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))
        surface.blit(label, (self.top_left_x + self.play_width / 2 - (label.get_width() / 2), 30))
        for i in range(len(grid.grid)):
            for j in range(len(grid.grid[i])):
                pygame.draw.rect(surface, grid.grid[i][j],
                                 (self.top_left_x + j * self.block_size, self.top_left_y + i * self.block_size,
                                  self.block_size, self.block_size), 0)
        grid.draw(surface, self.top_left_x, self.top_left_y, self.play_width, self.play_height, self.block_size)
        pygame.draw.rect(surface, (255, 0, 0), (self.top_left_x, self.top_left_y, self.play_width, self.play_height), 5)
        self.draw_next_shape(surface, next_piece)

    def draw_next_shape(self, surface, shape):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))
        start_x = self.top_left_x + self.play_width + 50
        start_y = self.top_left_y + self.play_height / 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color,
                                     (start_x + j * self.block_size, start_y + i * self.block_size,
                                      self.block_size, self.block_size), 0)
        surface.blit(label, (start_x + 10, start_y - 30))
