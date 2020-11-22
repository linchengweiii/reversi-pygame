import numpy as np
import random
import pygame
from pygame.constants import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION

class Point():
    def __init__(self, r, c):
        self.r = r
        self.c = c

class InvalidPositionError(Exception):
    pass

class BaseAgent():
    def __init__(self, rows_n, cols_n, width , height):
        self.rows_n = rows_n
        self.cols_n = cols_n
        self.block_len = 0.8 * min(height, width)/len(cols)
        self.col_offset = (width - height)/2 + 0.1 * min(height, width) + 0.5 * self.block_len
        self.row_offset = 0.1 * min(height, width) + 0.5 * self.block_len
        

    def step(self, reward, obs):
        """
        step()

        Parameters
        ----------
        reward : 
            score
        obs    :  dict{}
            64 blocks, value: [-1, 0 ,1, 2]
                    -1 : black
                     0 : empty
                     1 : white
                     2 : mouse pos

        Returns
        -------
        list: [tuple, event.type]
            (x, y) represents position, where (0, 0) mean top left. 
                x: go right
                y: go down
            event.type: [MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION]
                non human agent uses MOUSEBUTTONDOWN
        """

        raise NotImplementError()
    
class HumanAgent(BaseAgent):
    def step(self, reward, obs):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                return [event.pos, event.type]


class RandomAgent(BaseAgent):
    def step(self, reward, obs):
        """
        """
        return (self.col_offset + random.randint(0, self.cols_n-1) * self.block_len, self.row_offset + random.randint(0, self.rows_n-1) * self.block_len)

if __name__ == "__main__":
    agent = RandomAgent()
    print(agent.step(None, None))