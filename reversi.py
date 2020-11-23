import pygame
import sys
import numpy as np
from pygamewrapper import PyGameWrapper
from reversi_board import ReversiBoard
import utils

class Reversi(PyGameWrapper):
    """
        game_state:
            -1: dark side
            0: no piece
            1: light side
    """
    BG_COLOR = (255, 255, 255)
    FONT = 'font/OpenSans-Regular.ttf'
    def __init__(self, width=600, height=600, time_limit=30000, bg_color=BG_COLOR, font=FONT):
        screen_dim = (width, height)
        self.side_length = min(width, height)
        if width >= height:
            self.top_left = (0.5 * (width - height), 0)
        else:
            self.top_left = (0, 0.5 * (height - width))

        pygame.font.init()
        self.board = ReversiBoard(self.side_length, self.top_left)

        actions = self._init_action_set()
        super().__init__(width, height, actions=actions)

        self.bg_color = bg_color
        self.font = font
        self.last_label = '1A'
        self.cur_player = -1
        self.prev_action_time = 0
        self.time_limit = time_limit
        self.time_left = {-1: time_limit, 1: time_limit}

    def _init_action_set(self):
        actions = {}
        for i, row in enumerate(self.board.rows):
            for j , col in enumerate(self.board.cols):
                x = 0.1 * self.side_length + 0.8 * (j+0.5) / len(self.board.cols) * self.side_length
                y = 0.1 * self.side_length + 0.8 * (i+0.5) / len(self.board.rows) * self.side_length
                actions[row+col] = utils.element_wise_addition(self.top_left, (x, y))
        return actions

    def _handle_player_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                try:
                    if self.get_game_state()[self.board.enum[self.last_label]] == 2:
                        self.board.update(self.last_label, 0)
                    label = self.pos2label(event.pos)
                    if self._is_available(label):
                        self.last_label = label
                        self.board.update(label, 2)

                except utils.ValueOutOfRange:
                    pass

            elif (event.type == pygame.MOUSEBUTTONDOWN or
                  event.type == pygame.USEREVENT):
                try:
                    label = self.pos2label(event.pos)
                    if self._is_available(label, flip=True):
                        cur_time = pygame.time.get_ticks()
                        self.time_left[self.cur_player] -= cur_time - self.prev_action_time
                        self.prev_action_time = cur_time

                        self.board.update(label, self.cur_player)
                        self.cur_player *= -1

                        if len(self._get_available_actions()) <= 0:
                            self.cur_player *= -1
                            raise utils.NoAvailableAction()
                    else:
                        raise utils.InvalidAction()

                except utils.ValueOutOfRange:
                    raise utils.ValueOutOfRange()

    def _update_scores(self):
        x, y = 0, 0
        for r in self.board.rows:
            for c in self.board.cols:
                status = self.get_game_state()[self.board.enum[r+c]]
                if status == -1:
                    x += 1
                elif status == 1:
                    y += 1
        
        self.scores[-1] = x
        self.scores[1] = y

    def pos2label(self, pos):
        """
        Change the screen position to the label on the board.
        """
        pos = tuple([p - tl for p, tl in zip(pos, self.top_left)])

        if (pos[0] < 0 or pos[0] > self.side_length or
            pos[1] < 0 or pos[1] > self.side_length):
            raise utils.ValueOutOfRange()

        return self.board.pos2label(pos)

    def _is_available(self, label, flip=False):
        """
        Check if is able to place a piece on the label.

        Parameters
        ----------
        label: str
            The reference position
        flip: bool
            Flip the pieces or not

        Return
        ------
        bool
            Whether able to place the piece or not
        """
        status = self.get_game_state()
        if status[self.board.enum[label]] == 2 and flip == False:
            return True

        if status[self.board.enum[label]] == 0 or status[self.board.enum[label]] == 2:
            return self._check_around(label, flip=flip)

        return False

    def _check_around(self, label, flip):
        """
        Check the 3x3 blocks centered by label are occupied by the opponent or not.
        Run through that direction if the block on that direction is occupied by the opponent.

        Parameters
        ----------
        label: str
            The reference position
        flip: bool
            Flip the pieces or not

        Return
        ------
        bool
            Whether able to flip or not

        """
        is_avail = False
        status = self.get_game_state()
        row = int(self.board.enum[label] // len(self.board.cols))
        col = int(self.board.enum[label] % len(self.board.cols))
        for i in range(-1, 2):
            if row+i < 0 or row+i >= len(self.board.rows): continue

            for j in range(-1, 2):
                if col+j < 0 or col+j >= len(self.board.cols): continue

                label = self.board.rows[row+i] + self.board.cols[col+j]
                if status[self.board.enum[label]] == -1 * self.cur_player:
                    if self._check_direction(row, col, i, j, flip=flip):
                        is_avail = True
                    
        return is_avail

    def _check_direction(self, row, col, dx, dy, flip):
        """
        Check each direction whether is able to flip pieces or not.

        Parameters
        ----------
        row, col: int
            The position to start from
        dx, dy: int
            The direction to go through
        flip: bool
            Flip the pieces or not

        Return
        ------
        bool
            Whether able to flip or not

        """
        is_avail = False
        status = self.get_game_state()
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < len(self.board.rows) and 0 <= col+y[-1] < len(self.board.cols):
            label = self.board.rows[row+x[-1]] + self.board.cols[col+y[-1]]
            if status[self.board.enum[label]] == 0:
                break
            if status[self.board.enum[label]] == self.cur_player:
                if flip:
                    for r, c in zip(x, y):
                        self.board.update(self.board.rows[row+r]+self.board.cols[col+c], self.cur_player)
                    is_avail = True
                    break
                else:
                    return True

            x.append(x[-1] + dx)
            y.append(y[-1] + dy)

        return is_avail

    def _get_available_actions(self):
        avail = []
        for row in self.board.rows:
            for col in self.board.cols:
                if self._is_available(row+col):
                    avail.append(row+col)
                
        return avail

    def get_game_state(self):
        return self.board.status

    def get_actions(self):
        return self.actions

    def init(self):
        self.board.reset_status()

        self.time_left = {-1: self.time_limit, 1: self.time_limit}

        init_status = [('4D', 1), ('4E', -1), ('5D', -1), ('5E', 1)]
        for s in init_status:
            self.board.update(*s)

        self._update_scores()

        self.screen.fill(self.bg_color)
        self.board.draw_board(self.screen)
        self.board.draw_pieces(self.screen)

    def game_over(self):
        if self._time_out():
            self.winner = -1 * self.cur_player
            self._display_game_over()
            return True

        elif len(self._get_available_actions()) > 0:
            return False

        else:
            if self.scores[1] > self.scores[-1]:
                self.winner = 1
            elif self.scores[-1] > self.scores[1]:
                self.winner = -1

            self._display_game_over()
            return True

    def _display_game_over(self):
        """
        Display 'GAME OVER' on the screen 
        """
        font = pygame.font.Font(self.font, 72)
        text = font.render('GAME OVER', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = utils.element_wise_addition(self.top_left, (0.5 * self.side_length, 0.5 * self.side_length))
        self.screen.blit(text, text_rect)

    def step(self, dt):
        self._update_time_left()
        self._display_scores_and_time_left()

        try:
            self._handle_player_events()
            self._update_scores()
            self.board.draw_board(self.screen)
            self.board.draw_pieces(self.screen)
            self._display_scores_and_time_left()
            self._display_current_player()

        except utils.ValueOutOfRange:
            raise utils.ValueOutOfRange()

        except utils.InvalidAction:
            raise utils.InvalidAction()

        except utils.NoAvailableAction:
            self._update_scores()
            self.board.draw_board(self.screen)
            self.board.draw_pieces(self.screen)
            self._display_scores_and_time_left()
            self._display_current_player()
            raise utils.NoAvailableAction()

    def _time_out(self):
        """
        Gets the time left, return true if no time left.
        """
        if pygame.time.get_ticks() - self.prev_action_time > self.time_left[self.cur_player]:
            return True
        return False

    def _update_time_left(self):
        """
        Update the time left to the time left on the screen on date.
        """
        if pygame.time.get_ticks() - self.prev_action_time > self.time_left[self.cur_player] % 1000:
            self.time_left[self.cur_player] -= pygame.time.get_ticks() - self.prev_action_time
            self.prev_action_time = pygame.time.get_ticks()

    def _display_scores_and_time_left(self):
        """
        Dispaly scores and time left for both players.
        """
        text_colors = [[(255,160,122), (255,160,122)], [(0, 0, 0), (255, 255, 255)]]
        time_left = {key: max(0, int(self.time_left[key] // 1000)) for key in self.time_left}
        for i, display_dict in enumerate((time_left, self.scores)):
            for j, (player, text_color) in enumerate(zip(display_dict, text_colors[i])):
                font = pygame.font.Font(self.font, 24)
                text = font.render(str(display_dict[player]), True, text_color)
                text_rect = text.get_rect()
                text_rect.center = utils.element_wise_addition(self.top_left, (abs(0.1*(i+1)-j) * self.side_length, 0.95 * self.side_length))
                self.screen.blit(text, text_rect)

    def _display_current_player(self):
        """
        Display who's turn to play.
        """
        content = {-1: 'Black\'s turn.', 1: 'White\'s turn.'}
        text_color = {-1: (0, 0, 0), 1: (255, 255, 255)}
        font = pygame.font.Font(self.font, 24)
        text = font.render(content[self.cur_player], True, text_color[self.cur_player])
        text_rect = text.get_rect()
        text_rect.center = utils.element_wise_addition(self.top_left, (0.5 * self.side_length, 0.95 * self.side_length))
        self.screen.blit(text, text_rect)


if __name__ == '__main__':
    pygame.init()
    game = Reversi(width=600, height=600)
    game.screen = pygame.display.set_mode(game.get_screen_dims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while game.game_over() == False:
        dt = game.clock.tick_busy_loop(30)
        try:
            game.step(dt)
            pygame.display.update()
        except utils.ValueOutOfRange:
            pass
        except utils.InvalidAction:
            pass
        except utils.NoAvailableAction:
            pass
    
    for _ in range(10000):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

