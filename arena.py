import importlib
from agent.base_agent import RandomAgent, HumanAgent, BaseAgent
from reversi import Reversi
from env import Environment
from reversi_board import ReversiBoard
import pygame
import utils

width = 600
height = 600
game = Reversi(width = width, height = height)
play_ground = Environment(game, force_fps = False)
rev_board = ReversiBoard()



# our Random Agent!
random_agent1 = RandomAgent()
#random_agent1 = RandomAgent(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)
random_agent2 = RandomAgent(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)

reward1 = 0
reward2 = 0

# init agent and game.
play_ground.init()
play_ground.display_screen = True


def run_agent(agent: BaseAgent, reward: dict, obs: dict):
    action, event_type = random_agent1.step(reward, obs)
    reward = play_ground.act(action, event_type) # reward after an action
    return reward

# start our loop
score = 0.0
for i in range(1):
    # if the game is over
    if play_ground.game_over():
        play_ground.reset_game()
    while play_ground.game_over() == False:
        if (i % 2 == 0):
            obs = play_ground.get_game_state()
            while(1):
                try:
                    reward1 = run_agent(random_agent1, reward1, obs)
                    break
                except utils.ValueOutOfRange:
                    print("invalid action! retry!")
        else:
            obs = play_ground.get_game_state()
            while(1):
                try:
                    reward2 = run_agent(random_agent2, reward2, obs)
                    break
                except utils.ValueOutOfRange:
                    print("invalid action! retry!")     
    score = game.getScore()


