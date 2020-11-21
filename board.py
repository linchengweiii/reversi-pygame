import pygame

class Board(object):
    BG_COLOR = (46, 189, 87) # GREEN
    BORDER_COLOR = (139, 69, 19) # BROWN
    LINE_COLOR = (0, 0, 0) # BLACK
    TEXT_COLOR = (255, 255, 255) # WHITE
    FONT = 'font/OpenSans-Regular.ttf'
    def __init__(self, side_length, top_left, rows, cols, font=FONT,
                 bg_color=BG_COLOR, border_color=BORDER_COLOR,
                 line_color=LINE_COLOR, text_color=TEXT_COLOR):

        self.side_length = side_length
        self.top_left = top_left

        self.rows = rows
        self.cols = cols
        self.n_blocks = len(self.rows) * len(self.cols)

        self.bg_color = bg_color
        self.border_color = border_color
        self.line_color = line_color
        self.text_color = text_color

        min_side = min(len(self.rows), len(self.cols))
        self.block_size = 0.8 * self.side_length / min_side
        self.font = pygame.font.Font(font, int(0.4 * self.block_size))

        self.enum = {}
        self._enum()

        self.status = {}
        for i in range(self.n_blocks):
            self.status[i] = 0

    def _enum(self):
        for i, r in enumerate(self.rows):
            for j, c in enumerate(self.cols):
                self.enum[r+c] = i*len(self.rows)+j

    def draw_board(self, screen):
        self.board_size = (self.side_length, self.side_length)
        self.border_size = (0.1 * self.side_length, self.side_length) 

        translation = (0.9 * self.side_length, 0)
        top_left = self.top_left
        top_right = tuple([sum(x) for x in zip(top_left, translation)])
        bottom_left = tuple([sum(x) for x in zip(top_left, reversed(translation))])

        pygame.draw.rect(screen, self.bg_color, (top_left, self.board_size))
        pygame.draw.rect(screen, self.border_color, (top_left, self.border_size))
        pygame.draw.rect(screen, self.border_color, (top_right, self.border_size))
        pygame.draw.rect(screen, self.border_color, (top_left, tuple(reversed(self.border_size))))
        pygame.draw.rect(screen, self.border_color, (bottom_left, tuple(reversed(self.border_size))))

        for i, row in enumerate([''] + self.rows):
            x = 0.1 * self.side_length + 0.8 * i / len(self.rows) * self.side_length
            pygame.draw.line(screen, self.line_color, (x, 0.1 * self.side_length), (x, 0.9 * self.side_length))

            self._draw_label(screen, row, (x - 0.05 * self.side_length, 0.05 * self.side_length))


        for i , col in enumerate([''] + self.cols):
            y = 0.1 * self.side_length + 0.8 * i / len(self.cols) * self.side_length
            pygame.draw.line(screen, self.line_color, (0.1 * self.side_length, y), (0.9 * self.side_length, y))

            self._draw_label(screen, col, (0.05 * self.side_length, y - 0.05 * self.side_length))


    def _draw_label(self, screen, text_str, position):
        text =  self.font.render(text_str, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = position
        screen.blit(text, text_rect)


    def draw_pieces(self, screen):
        """
        This function draw the pieces on the board.

        This is game dependent.

        """
        raise NotImplementedError("Please override this method")

    def update(self, block, new_status):
        if isinstance(block, str):
            block = self.enum[block]

        self.status[block] = new_status
