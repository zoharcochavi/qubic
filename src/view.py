import pygame as pg
from util import GameProperties

IMG_RATIO = 118 / 84
FINAL_IMG_RATIO = 0.56

NEW_IMG_HEIGHT = 40


class Drawer:
    def __init__(self, RATIO=16 / 10, HEIGHT=900):
        # general settings
        self.button_group = None

        self.HEIGHT = HEIGHT
        self.WIDTH = RATIO * self.HEIGHT

        self.DIM_BUTTONS_WIDTH = 120
        self.DIM_BUTTONS_HEIGHT = 50
        self.TOOLBAR_HEIGHT = 100
        self.STATUS_HEIGHT = 100

        # colors
        self.BG = (52, 52, 52)
        self.BG_ALT = (80, 80, 80)
        self.LINE_COLOR = (144, 144, 144)

        # font
        self.mono_font = pg.font.Font("assets/FiraCode.ttf", 30)

        # grid settings
        self.h_padding_grid = 100
        self.margin_grid = 50
        self.line_thickness_grid = 2

        # pygame init
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pg.display.set_caption("My Tic Tac Toe")

    def parse_grid_settings(self):
        """
        Parses the settings defined in the init function to generate some parameters to improve quality of life
        """
        self.grid_left = self.h_padding_grid
        self.grid_right = self.WIDTH - self.h_padding_grid
        self.grid_top = self.DIM_BUTTONS_HEIGHT + self.STATUS_HEIGHT
        self.grid_bottom = self.HEIGHT - self.TOOLBAR_HEIGHT

        dim = GameProperties.get_instance().dim

        self.grid_cell_width = (self.grid_right - self.grid_left) / dim
        self.grid_cell_height = (self.grid_bottom - self.grid_top) / dim

    def draw_grid(self, margin=7):
        """
        Draws the grid according to the given parameters
        """
        self.screen.fill(self.BG)
        self.screen.fill(self.BG_ALT, (self.h_padding_grid, self.DIM_BUTTONS_HEIGHT + self.STATUS_HEIGHT,
                                       self.WIDTH - 2 * self.h_padding_grid,
                                       self.HEIGHT - self.DIM_BUTTONS_HEIGHT - self.TOOLBAR_HEIGHT - self.STATUS_HEIGHT))

        width = self.grid_right - self.grid_left
        height = self.grid_bottom - self.grid_top

        left = self.grid_left + margin
        right = self.grid_right - margin
        top = self.grid_top + margin
        bottom = self.grid_bottom - margin

        dim = GameProperties.get_instance().dim

        # drawing vertical & horizontal lines
        for i in range(1, dim):
            # vertical line
            pg.draw.line(self.screen, self.LINE_COLOR,
                         # start and stop coordinates (x, y)
                         (width / dim * i + self.grid_left, top), (width / dim * i + self.grid_left, bottom),
                         self.line_thickness_grid)
            # horizontal line
            pg.draw.line(self.screen, self.LINE_COLOR,
                         (left, height / dim * i + self.grid_top), (right, height / dim * i + self.grid_top),
                         self.line_thickness_grid)

    def init_home_window(self):
        """
        Initializes the home window with a welcome status and buttons for selecting the board dimesnion.
        """
        self.draw_welcome_status()
        self.draw_dim_buttons()

    def draw_welcome_status(self):
        """
        Draws the welcoming text at the top of the window.
        """
        self.screen.fill(self.BG)

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore " \
               "et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut " \
               "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse " \
               "cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in " \
               "culpa qui officia deserunt mollit anim id est laborum."

        # keep margin low for text to be at top of window
        margin = 100
        rect = pg.Rect(margin, margin,
                       self.WIDTH - 2 * margin, self.HEIGHT / 2)
        self.draw_text(text, (255, 255, 255), rect, self.mono_font)

        pg.display.update()

    def draw_dim_buttons(self):
        """
        Draws draws text and buttons that allow user to select board dimension.
        """
        text = self.mono_font.render("Please select a board dimension:", True, (255, 255, 255))

        # place text on center-bottom part of window
        text_rect = text.get_rect(center=(self.WIDTH / 2, self.HEIGHT * 3 / 4))

        self.screen.blit(text, text_rect)

        # add buttons
        buttons_distance = 60
        distance_from_text = 50
        # create rectangle for button
        rect_3 = pg.Rect(self.WIDTH / 2 - self.DIM_BUTTONS_WIDTH * 3 / 2 - buttons_distance,
                         self.HEIGHT * 3 / 4 + distance_from_text,
                         self.DIM_BUTTONS_WIDTH, self.DIM_BUTTONS_HEIGHT)
        # draw button
        self.draw_dim_button('3 x 3', rect_3)

        rect_4 = pg.Rect(self.WIDTH / 2 - self.DIM_BUTTONS_WIDTH / 2, self.HEIGHT * 3 / 4 + distance_from_text,
                         self.DIM_BUTTONS_WIDTH, self.DIM_BUTTONS_HEIGHT)
        self.draw_dim_button('4 x 4', rect_4)
        rect_5 = pg.Rect(self.WIDTH / 2 + self.DIM_BUTTONS_WIDTH / 2 + buttons_distance,
                         self.HEIGHT * 3 / 4 + distance_from_text,
                         self.DIM_BUTTONS_WIDTH, self.DIM_BUTTONS_HEIGHT)
        self.draw_dim_button('5 x 5', rect_5)

        pg.display.update()

        # keep buttons rectangles (with associated dimensions) to determine if user clicked on them
        self.button_group = [
            [rect_3, 3],
            [rect_4, 4],
            [rect_5, 5]
        ]

    def draw_dim_button(self, text, rect, rect_color=None, margin_color=(0, 0, 0), text_color=(255, 255, 255)):
        """
        Draws button with border and text at given position (rect)
        @param rect: pygame.Rect or 4-tuple (float, float, float, float)
        """
        if rect_color is None:
            rect_color = self.BG_ALT

        # draw button
        rect_obj = pg.draw.rect(self.screen, rect_color, rect)
        # draw border
        pg.draw.rect(self.screen, margin_color, rect, 2)

        text_surface_obj = self.mono_font.render(text, True, text_color)
        # put text in center of button
        text_rect = text_surface_obj.get_rect(center=rect_obj.center)

        self.screen.blit(text_surface_obj, text_rect)

    def init_window(self):
        """
        Initializes the window with the grid and status
        """
        self.parse_grid_settings()
        self.draw_grid()
        self.draw_status(1, 0, None, None)

    def draw_status(self, turn_num, sub_turn_num, winner, coords):
        """
        Draws the status bar
        TODO Separate the status- and toolbars
        """
        if winner is None:
            if turn_num % 2 == 0:
                message = "0's turn"
            else:
                message = "1's turn"

            if sub_turn_num % 2 == 1:
                message += " again"

        elif winner == '-':
            message = "Game draw!"
        else:
            message = ("1" if winner == "x" else "0") + " won!"

        self.draw_status_message(message)

    def draw_final(self, board, padding=32):
        for row, li in enumerate(board.final):
            for col, el in enumerate(li):
                if el:
                    posx = self.grid_left + self.grid_cell_width * col + self.line_thickness_grid
                    posy = self.grid_top + self.grid_cell_height * row + self.line_thickness_grid

                    self.screen.fill(self.BG_ALT, (posx, posy, self.grid_cell_width - self.line_thickness_grid,
                                                   self.grid_cell_height - self.line_thickness_grid))
                    self.screen.fill(self.BG_ALT,
                                     (posx, posy,
                                      self.grid_cell_width - self.line_thickness_grid,
                                      self.grid_cell_height - self.line_thickness_grid))
                    pg.display.update()

                    self.draw_xo_at(board, posx + padding, posy + padding,
                                    ox_override=str.capitalize(board.board[row][col][0]), final=True, height=64)

    def draw_quantum_xo(self, board, row, col, padding=15):
        """
        Draws an X or O in the given (row, col) depending on the board state
        """
        posx = self.grid_left + self.grid_cell_width * col + ((len(board.board[row][col]) - 1) % 3) * (
                IMG_RATIO * NEW_IMG_HEIGHT + padding) + padding
        border_y = int((len(board.board[row][col]) - 1) / 3) * NEW_IMG_HEIGHT
        posy = self.grid_top + self.grid_cell_height * row + border_y + padding

        self.draw_xo_at(board, posx, posy)

    def draw_xo_at(self, board, posx, posy, ox_override=None, final=False, height=NEW_IMG_HEIGHT):
        correct_turn_num = board.turnNum

        if board.subTurnNum % 2 == 0:
            correct_turn_num -= 1

        if ox_override is not None:
            asset = ox_override
        else:
            asset = "X" if correct_turn_num % 2 == 1 else "O"

        # todo: add all remaining pics
        img = pg.image.load("assets/" + asset + ("F" if final else str(correct_turn_num)) + ".png")
        img = pg.transform.smoothscale(img, ((FINAL_IMG_RATIO if final else IMG_RATIO) * height, height))

        self.screen.blit(img, (posx, posy))

        pg.display.update()

    def draw_status_message(self, message):
        """
        General method for drawing a message at the top of the screen
        """
        # setting the font properties like
        # color and WIDTH of the text
        text = self.mono_font.render(message, True, (255, 255, 255))

        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill(self.BG, (0, self.DIM_BUTTONS_HEIGHT, self.WIDTH, self.STATUS_HEIGHT))
        text_rect = text.get_rect(center=(self.WIDTH / 2, self.DIM_BUTTONS_HEIGHT + self.STATUS_HEIGHT / 2))
        self.screen.blit(text, text_rect)
        pg.display.update()

    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted
    def draw_text(self, text, color, rect, font, line_spacing=10, center_text=True):
        """
        Wraps and draws text at position.
        @param rect: pygame.Rect (or float 4-tuple) specifies region in which text is to be drawn.
        """
        rect = pg.Rect(rect)
        y = rect.top

        # get the height of the font
        font_height = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + font_height > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            image = font.render(text[:i], True, color)

            if center_text:
                image_rect = image.get_rect(center=((rect.left + rect.right) / 2, y))
            else:
                image_rect = (rect.left, y)

            self.screen.blit(image, image_rect)
            y += font_height + line_spacing

            # remove the text we just blitted
            text = text[i:]

        return text
