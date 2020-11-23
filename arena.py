from agent.base_agent import RandomAgent, HumanAgent, BaseAgent
from reversi import Reversi
from env import Environment
from reversi_board import ReversiBoard
import pygame
import utils
import time
import importlib
import argparse


# our Random Agent!
# You can also test with HumanAgent
# agent1 = RandomAgent(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)
# agent2 = RandomAgent(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = width, height = height)

def run_agent(agent: BaseAgent, reward: dict, obs: dict):
    action, event_type = agent.step(reward, obs)
    reward = play_ground.act(action, event_type) # reward after an action
    return reward

def main(play_ground, agent1, agent2, rounds):
    reward1 = 0
    reward2 = 0

    # start our loop
    for i in range(rounds):
        if play_ground.game_over():
            play_ground.reset_game()

        run_iter = 0
        while play_ground.game_over() == False:
            if (run_iter % 2 == 0):
                obs = play_ground.get_game_state()
                while True:
                    try:
                        reward1 = run_agent(agent1, reward1, obs)
                        if reward1[-1] != 0:
                            break
                    except (utils.ValueOutOfRange, utils.InvalidAction) as e:
                        # print("invalid action! retry!")
                        pass
                    except utils.NoAvailableAction:
                        # print("ignore black action")
                        run_iter += 1
                        break
            else:
                obs = play_ground.get_game_state()
                while True:
                    try:
                        # time.sleep(0.1)
                        reward2 = run_agent(agent2, reward2, obs)
                        if reward2[1] != 0:
                            break
                    except (utils.ValueOutOfRange, utils.InvalidAction) as e:
                        # print("invalid action! retry!") 
                        pass
                    except utils.NoAvailableAction:
                        # print("ignore white action")
                        run_iter += 1
                        break
            run_iter += 1 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent1', default="base_agent.HumanAgent")
    parser.add_argument('--agent2', default="base_agent.RandomAgent")
    parser.add_argument('--width', default=600, type=int)
    parser.add_argument('--height', default=600, type=int)
    parser.add_argument('--rounds', default=10, type=int)
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()

    game = Reversi(width = args.width, height = args.height)
    play_ground = Environment(game, force_fps = False)
    rev_board = ReversiBoard()

    # init agent and game.
    play_ground.init()
    play_ground.display_screen = not args.headless

    agent1_module = importlib.import_module("agent."+args.agent1.split('.')[0])
    agent2_module = importlib.import_module("agent."+args.agent2.split('.')[0])

    agent1 = getattr(agent1_module, args.agent1.split('.')[1])(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = args.width, height = args.height)
    agent2 = getattr(agent2_module, args.agent2.split('.')[1])(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = args.width, height = args.height)
    main(play_ground, agent1, agent2, args.rounds)

