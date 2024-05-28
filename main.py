import pygame
import random
import numpy as np
from tetris_game import *
from dqn_agent import DQNAgent
from tetris_agent import TetrisAgent

MODEL_WEIGHTS_FILE = 'tetris_dqn_weights.h5'

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

    # Load the model weights if they exist
    try:
        dqn_agent.load(MODEL_WEIGHTS_FILE)
        print("Model weights loaded successfully.")
    except Exception as e:
        print(f"Error loading model weights: {e}")

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

            cleared_rows = clear_rows(grid, locked_positions)
            score += cleared_rows * 10
            print(f"Rows cleared: {cleared_rows}, Score: {score}")

            # Replay and log the loss value
            if len(dqn_agent.memory) > batch_size:
                dqn_agent.replay(batch_size)

        draw_window(screen, grid, score)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("You Lost", 80, WHITE, screen)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    # Save the model weights after each game
    dqn_agent.save(MODEL_WEIGHTS_FILE)
    print("Model weights saved successfully.")

    return score

def main_menu():
    global screen
    pygame.init()
    pygame.font.init()  # Initialize the font module
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    
    while True:
        score = main()
        print(f"Game over! Final Score: {score}")
        pygame.time.delay(2000)  # Wait for 2 seconds before starting the next game

if __name__ == "__main__":
    main_menu()
