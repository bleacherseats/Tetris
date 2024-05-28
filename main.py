import pygame
import random
from tetris_game import *
from dqn_agent import DQNAgent
from tetris_agent import TetrisAgent

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Tetrimino(5, 0)
    next_piece = Tetrimino(5, 0)
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    agent = TetrisAgent()
    state_size = GRID_WIDTH * GRID_HEIGHT
    action_size = 4  # Number of possible actions
    dqn_agent = DQNAgent(state_size, action_size)
    batch_size = 32

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game_state = convert_shape_format(current_piece)
        action = agent.choose_action(game_state)

        if action == 'left':
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
        elif action == 'right':
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
        elif action == 'down':
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
        elif action == 'rotate':
            current_piece.rotate()
            if not valid_space(current_piece, grid):
                current_piece.rotate()

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = COLORS[current_piece.color]

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = COLORS[current_piece.color]
            current_piece = next_piece
            next_piece = Tetrimino(5, 0)
            change_piece = False

            score += clear_rows(grid, locked_positions) * 10

        draw_window(screen, grid, score)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("You Lost", 80, WHITE, screen)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

def main_menu():
    global screen
    pygame.init()
    pygame.font.init()  # Initialize the font module
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    
    run = True
    while run:
        screen.fill(BLACK)
        draw_text_middle('Press Any Key To Play', 60, WHITE, screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

if __name__ == "__main__":
    main_menu()
