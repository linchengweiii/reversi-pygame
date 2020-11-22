import importlib
from agent.base_agent import RandomAgent, HumanAgent
from reversi import Reversi
from env import Environment
from reversi_board import ReversiBoard
import pygame

pygame.init()
width = 600
height = 600
game = Reversi(width = width, height = height)
play_ground = Environment(game)
rev_board = ReversiBoard()



# our Random Agent!
random_agent1 = RandomAgent(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)
random_agent2 = RandomAgent(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)

reward1 = 0
reward2 = 0

# init agent and game.
play_ground.init()
play_ground.display_screen = True


# start our loop
score = 0.0
for i in range(100):
    # if the game is over
    if play_ground.game_over():
        play_ground.reset_game()
    while play_ground.game_over() == False:
        if (i % 2 == 0):
            obs = play_ground.get_game_state()
            action, event_type = random_agent1.step(reward1, obs)
            reward1 = play_ground.act(action, event_type) # reward after an action
        else:
            obs = play_ground.get_game_state()
            action, event_type = random_agent2.step(reward2, obs)
            reward2 = play_ground.act(action, event_type) # reward after an action
    #score = game.getScore()


