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
    def __init__(self, width=600, height=600, bg_color=BG_COLOR, font=FONT):
        screen_dim = (width, height)
        self.side_length = min(width, height)
        if width >= height:
            self.top_left = (0.5 * (width - height), 0)
        else:
            self.top_left = (0, 0.5 * (height - width))

        pygame.font.init()
        self.board = ReversiBoard(self.side_length, self.top_left)

        actions = self.board.enum
        super().__init__(width, height, actions=actions)

        self.bg_color = bg_color
        self.font = pygame.font.Font(font, 24)
        self.last_label = '1A'
        self.cur_player = -1

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    label = self.pos2label(event.pos)
                    if self._is_available(label, flip=True):
                        self.board.update(label, self.cur_player)
                        if len(self._get_available_actions()) > 0:
                            self.cur_player *= -1

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
        pos = tuple([p - tl for p, tl in zip(pos, self.top_left)])

        if (pos[0] < 0 or pos[0] > self.side_length or
            pos[1] < 0 or pos[1] > self.side_length):
            raise utils.ValueOutOfRange()

        return self.board.pos2label(pos)

    def _is_available(self, label, flip=False):
        status = self.get_game_state()
        if status[self.board.enum[label]] == 2 and flip == False:
            return True

        if status[self.board.enum[label]] == 0 or status[self.board.enum[label]] == 2:
            return self._check_around(label, flip=flip)

        return False

    def _check_around(self, label, flip):
        is_avail = False
        status = self.get_game_state()
        row = int(self.board.enum[label] // len(self.board.rows))
        col = int(self.board.enum[label] % len(self.board.rows))
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
        init_status = [('4D', 1), ('4E', -1), ('5D', -1), ('5E', 1)]
        for s in init_status:
            self.board.update(*s)

        self._update_scores()

        self.screen.fill(self.bg_color)
        self.board.draw_board(self.screen)
        self.board.draw_pieces(self.screen)

    def game_over(self):
        if len(self._get_available_actions()) > 0:
            return False
        return True

    def step(self, dt):
        self._handle_player_events()
        self._update_scores()
        self.board.draw_board(self.screen)
        self.board.draw_pieces(self.screen)
        self._display_scores()
        self._display_current_palyer()

    def _display_scores(self):
        text_colors = [(0, 0, 0), (255, 255, 255)]
        for i, (player, text_color) in enumerate(zip(self.scores, text_colors)):
            text = self.font.render(str(self.scores[player]), True, text_color)
            text_rect = text.get_rect()
            text_rect.center = utils.element_wise_addition(self.top_left, (abs(0.2-i) * self.side_length, 0.95 * self.side_length))
            self.screen.blit(text, text_rect)

    def _display_current_palyer(self):
        content = {-1: 'Black\'s turn.', 1: 'White\'s turn.'}
        text_color = {-1: (0, 0, 0), 1: (255, 255, 255)}
        text = self.font.render(content[self.cur_player], True, text_color[self.cur_player])
        text_rect = text.get_rect()
        text_rect.center = utils.element_wise_addition(self.top_left, (0.5 * self.side_length, 0.95 * self.side_length))
        self.screen.blit(text, text_rect)

if __name__ == '__main__':
    pygame.init()
    game = Reversi(width=800, height=600)
    game.screen = pygame.display.set_mode(game.get_screen_dims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while game.game_over() != True:
        dt = game.clock.tick_busy_loop(30)
        try:
            game.step(dt)
            pygame.display.update()
        except utils.ValueOutOfRange:
            pass
