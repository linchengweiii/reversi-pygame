import pygame

class PyGameWrapper(object):
    def __init__(self, width, height, actions={}):
        self.width = width
        self.height = height
        self.screen_dim = (width, height)
        self.actions = actions

        self.scores = 0.0
        self.lives = 0
        self.screen = None
        self.clock = None
        self.allowed_fps = None
        self.NOOP = None

    def _setup(self):
        """
        Setups up the pygame env, the display and game clock.
        """
        pygame.init()
        self.screen = pygame.display.set_model(self.get_screen_dims(), 0, 32)
        self.clock = pygame.time.Clock()

    def _draw_frame(self, draw_screen):
        """
        Decides if the screen will be drawn.
        """
        if draw_screen:
            pygame.display.update()

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

    def get_score(self):
        """
        Return the current score of the game.

        Returns
        -------
        int 
            The current reward the agent has received since the last init() or reset() call.

        """
        return self.score

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
