import importlib
from agent.base_agent import RandomAgent, HumanAgent, BaseAgent
from reversi import Reversi
from env import Environment
from reversi_board import ReversiBoard
import pygame
import utils
import time

width = 600
height = 600
game = Reversi(width = width, height = height)
play_ground = Environment(game, force_fps = False)
rev_board = ReversiBoard()



# our Random Agent!
# You can also use HumanAgent
agent1 = HumanAgent()
#agent1 = RandomAgent(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)
agent2 = RandomAgent(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)

reward1 = 0
reward2 = 0

# init agent and game.
play_ground.init()
play_ground.display_screen = True


def run_agent(agent: BaseAgent, reward: dict, obs: dict):
    action, event_type = agent.step(reward, obs)
    reward = play_ground.act(action, event_type) # reward after an action
    return reward

# start our loop
score = 0.0
for i in range(1):
    # if the game is over
    if play_ground.game_over():
        play_ground.reset_game()
    run_iter = 0
    while play_ground.game_over() == False:
        if (run_iter % 2 == 0):
            print("black turn")
            obs = play_ground.get_game_state()
            while(1):
                try:
                    reward1 = run_agent(agent1, reward1, obs)
                    #print(reward1)
                    if reward1[-1] != 0:
                        break
                except (utils.ValueOutOfRange, utils.InvalidAction) as e:
                    # print("invalid action! retry!")
                    pass
                except utils.NoAvailableAction:
                    print("ignore black action")
                    
                    break
        else:
            print("white turn")
            obs = play_ground.get_game_state()
            while(1):
                try:
                    time.sleep(0.1)
                    reward2 = run_agent(agent2, reward2, obs)
                    #print(reward2)
                    if reward2[1] != 0:
                        break
                except (utils.ValueOutOfRange, utils.InvalidAction) as e:
                    # print("invalid action! retry!") 
                    pass
                except utils.NoAvailableAction:
                    print("ignore white action")
                    
                    break  
        run_iter += 1 
    #score = game.getScore()


