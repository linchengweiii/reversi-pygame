import pygame
from pygame.constants import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION

class PyGameWrapper(object):
    def __init__(self, width, height, actions={}):
        self.width = width
        self.height = height
        self.screen_dim = (width, height)
        self.actions = actions

        self.scores = {}
        self.lives = 0
        self.screen = None
        self.clock = None

    def setup(self):
        """
        Setups up the pygame env, the display and game clock.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.get_screen_dims(), 0, 32)
        self.clock = pygame.time.Clock()

    def draw_frame(self, draw_screen):
        """
        Decides if the screen will be drawn.
        """
        if draw_screen:
            pygame.display.update()

    def set_action(self, pos, last_pos, event_type):
        """
        Push the actions to the pygame event qeueu.
        """
        if event_type == MOUSEMOTION:
            mm = pygame.event.Event(MOUSEMOTION, {'pos': pos})
            pygame.event.post(mm)

        if event_type == MOUSEBUTTONDOWN:
            md = pygame.event.Event(MOUSEBUTTONDOWN, {'pos': pos})
            mu = pygame.event.Event(MOUSEBUTTONUP, {'pos': last_pos})
            pygame.event.pos(md)
            pygame.event.pos(mu)

    def get_game_state(self):
        """
        Gets a non-visual state representation of the game.

        Returns
        -------
        dict or None
            dict if the game supports it and None otherwise.

        """
        return None

    def get_screen_dims(self):
        """
        Gets the screen dimensiions of the game in tuple form.

        Returns
        -------
        tuple of int
            (width, height)

        """
        return self.screen_dim

    def get_actions(self):
        """
        Gets the actions used within the game.

        Returns
        -------
        list of int

        """
        return self.actions.values()

    def init(self):
        """
        This is used to initialize the game.

        This is game dependent.
        """
        raise NotImplementedError("Please override this method")

    def reset(self):
        """
        Wraps the init() function, can be setup to reset certain portions of the game only if needed.
        """
        self.init()

    def get_scores(self):
        """
        Return the current score of the game.

        Returns
        -------
        int 
            The current reward the agent has received since the last init() or reset() call.

        """
        return self.scores

    def game_over(self):
        """
        Gets the status of the game, returns True if the game has hit a terminal state. False otherwise.

        This is game dependent.

        Returns
        -------
        bool

        """
        raise NotImplementedError("Please override this method")

    def step(self, dt):
        """
        This method steps the game forward one step in time equl to the dt parameter. The game does not run unless this method is called.

        Parameters
        ----------
        dt: integer
            This is the amount of time elapsed since the last frame in milliseconds.

        """
        raise NotImplementedError("Please override this method")
