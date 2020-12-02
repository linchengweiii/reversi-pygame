from agent.base_agent import RandomAgent, HumanAgent, BaseAgent
from reversi import Reversi
from env import Environment
from reversi_board import ReversiBoard
import pygame
import utils
import importlib
import argparse
from tqdm.auto import tqdm

class Arena(object):
    def __init__(self, playground, player1, player2):
        self.playground = playground
        self.player = {-1: player1, 1: player2}

    def run(self, n_rounds):
        n_rounds_black_wins = 0
        for i in tqdm(range(n_rounds)):
            reward = {-1: {}, 1: {}}
            if self.playground.game_over():
                self.playground.reset_game()

            player_index = -1
            while self.playground.game_over() == False:
                player_index, reward = self.step(self.player[player_index], reward)
            
            self.playground._draw_frame()

            if self.playground.game.winner == -1:
                n_rounds_black_wins += 1

        print ('Your win rate is', n_rounds_black_wins / n_rounds * 100, '%')


    def run_agent(self, agent, reward, obs):
        action, event_type = agent.step(reward, obs)
        reward = self.playground.act(action, event_type) # reward after an action
        return reward

    def step(self, agent, reward):
        player_index = -1 if agent.color == 'black' else 1
        obs = self.playground.get_game_state()
        while True:
            try:
                reward[player_index] = self.run_agent(agent, reward[player_index], obs)
                if reward[player_index][player_index] != 0:
                    return -1 * player_index, reward

            except (utils.ValueOutOfRange, utils.InvalidAction) as e:
                # print("invalid action! retry!")
                pass

            except utils.NoAvailableAction:
                # print("ignore black action")
                self.playground._get_reward()
                return player_index, reward


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent1', default="base_agent.HumanAgent")
    parser.add_argument('--agent2', default="base_agent.RandomAgent")
    parser.add_argument('--width', default=600, type=int)
    parser.add_argument('--height', default=600, type=int)
    parser.add_argument('--n_rounds', default=10, type=int)
    parser.add_argument('--time_limit', default=30000, type=int)
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()

    if args.headless:
        import os
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    game = Reversi(width = args.width, height = args.height, time_limit=args.time_limit)
    playground = Environment(game, force_fps = False)
    rev_board = ReversiBoard()

    # init agent and game.
    playground.init()
    playground.display_screen = True

    agent1_module = importlib.import_module("agent."+args.agent1.split('.')[0])
    agent2_module = importlib.import_module("agent."+args.agent2.split('.')[0])

    agent1 = getattr(agent1_module, args.agent1.split('.')[1])(color = "black", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = args.width, height = args.height)
    agent2 = getattr(agent2_module, args.agent2.split('.')[1])(color = "white", rows_n = len(rev_board.rows), cols_n = len(rev_board.cols), width = args.width, height = args.height)

    arena = Arena(playground, agent1, agent2)
    arena.run(args.n_rounds)

