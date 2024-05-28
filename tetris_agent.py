import random

class TetrisAgent:
    def __init__(self):
        pass

    def choose_action(self, game_state):
        # For simplicity, choose a random action
        actions = ['left', 'right', 'rotate', 'drop']
        return random.choice(actions)
