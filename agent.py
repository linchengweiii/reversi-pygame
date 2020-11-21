import numpy as np

class Point():
	def __init__(self, r, c):
		self.r = r
		self.c = c

class InvalidPositionError(Exception):
    pass

class BaseAgent():
    def __init__(self):
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.inv_rows_dict = {i:ct for ct, i in enumerate(rows)}
        self.inv_cols_dict = {i:ct for ct, i in enumerate(cols)}

    def pos2idx(self, position: Point):
    	"""
    	input: position
    	return the index to represent the position
    	"""
    	if position.r not in self.rows or position.c not in self.cols:
    		raise InvalidPositionError("input point is not valid, r should be in self.rows and c should be in self.cols")

    	return self.inv_rows_dict[position.r] * len(self.cols) + self.inv_cols_dict[position.c]  


    def step(self, reward, obs):
    	"""
    	reward:  score 
    	obs   :  
    	"""
    	raise NonImplementError
  	

class RandomAgent(BaseAgent):
	def __init__(self):
        super(self)

    def step(self, reward, obs):
    	"""
    	return action
    	"""
    	return self.pos2idx(Point(random.choice(self.rows), random.choice(self.cols)))


        