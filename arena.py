from agent.base_agent import RandomAgent, HumanAgent, BaseAgent
from reversi import Reversi
from env import Environment
from reversi_board import ReversiBoard
import pygame
import utils
import importlib
import argparse
from tqdm.auto import tqdm

def run_agent(agent: BaseAgent, reward: dict, obs: dict):
    action, event_type = agent.step(reward, obs)
    reward = play_ground.act(action, event_type) # reward after an action
    return reward

def main(play_ground, agent1, agent2, rounds):
    # start our loop
    n_black_wins = 0
    for i in tqdm(range(rounds)):
        reward1, reward2 = {}, {}
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
                        play_ground._get_reward()
                        run_iter += 1
                        break
            else:
                obs = play_ground.get_game_state()
                while True:
                    try:
                        reward2 = run_agent(agent2, reward2, obs)
                        if reward2[1] != 0:
                            break
                    except (utils.ValueOutOfRange, utils.InvalidAction) as e:
                        # print("invalid action! retry!") 
                        pass
                    except utils.NoAvailableAction:
                        # print("ignore white action")
                        play_ground._get_reward()
                        run_iter += 1
                        break
            run_iter += 1 
        
        play_ground._draw_frame()


        if game.winner == -1:
            n_black_wins += 1

    print ('Your win rate is', n_black_wins / rounds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent1', default="base_agent.HumanAgent")
    parser.add_argument('--agent2', default="base_agent.RandomAgent")
    parser.add_argument('--width', default=600, type=int)
    parser.add_argument('--height', default=600, type=int)
    parser.add_argument('--rounds', default=10, type=int)
    parser.add_argument('--time_limit', default=30000, type=int)
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()

    if args.headless:
        import os
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    game = Reversi(width = args.width, height = args.height, time_limit=args.time_limit)
    play_ground = Environment(game, force_fps = False)
    rev_board = ReversiBoard()

    # init agent and game.
    play_ground.init()
    play_ground.display_screen = True

    agent1_module = importlib.import_module("agent."+args.agent1.split('.')[0])
    agent2_module = importlib.import_module("agent."+args.agent2.split('.')[0])

    agent1 = getattr(agent1_module, args.agent1.split('.')[1])(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = args.width, height = args.height)
    agent2 = getattr(agent2_module, args.agent2.split('.')[1])(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = args.width, height = args.height)
    main(play_ground, agent1, agent2, args.rounds)

