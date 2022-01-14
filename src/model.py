import graph as graphlib
from superposition_solver import resolve_superposition
from util import id_to_position


class Board:
    def __init__(self):
        self.board = None
        self.final = None
        self.winner = None  # can either be 'o', 'x', or '-' for a draw
        self.turnNum = 1
        self.subTurnNum = 0
        self.prevSubTurnIndex = None
        self.graph = graphlib.Graph()

        self.reset()

    def reset(self):
        """
        Resets the board
        """
        # 2d array with empty lists in every cell
        self.board = [[[], [], []],
                      [[], [], []],
                      [[], [], []]]
        self.final = [[False] * 3, [False] * 3, [False] * 3]
        self.winner = None
        self.turnNum = 1
        self.subTurnNum = 0
        self.prevSubTurnIndex = None
        self.graph = graphlib.Graph()

    def check_win(self):
        """
        Checks which player has won, returns a tuple where the first element is the winner and the
        second a tuple with coordinates for which column/row/diagonal is the winning one
        """
        # check if there is already a winner
        if self.winner is not None:
            return self.winner, None

        # check that it is player's final move
        if self.subTurnNum == 0:
            # checking for winning rows
            for row in range(0, 3):
                if self.final[row][0] and self.final[row][1] and self.final[row][2] and \
                        (self.board[row][0] == self.board[row][1] == self.board[row][2]) and \
                        (self.board[row][0] is not None):
                    self.winner = self.board[row][0]
                    return self.winner, ((row, 0), (row, 2))

            # checking for winning columns
            for col in range(0, 3):
                if self.final[0][col] and self.final[1][col] and self.final[2][col] and \
                        (self.board[0][col] == self.board[1][col] == self.board[2][col]) and \
                        (self.board[0][col] is not None):
                    self.winner = self.board[0][col]
                    return self.winner, ((0, col), (2, col))

            # check for diagonal winners
            if self.final[0][0] and self.final[1][1] and self.final[2][2] and \
                    (self.board[0][0] == self.board[1][1] == self.board[2][2]) and \
                    (self.board[0][0] is not None):
                # game won diagonally left to right
                self.winner = self.board[0][0]
                return self.winner, ((0, 0), (2, 2))

            if self.final[0][2] and self.final[1][1] and self.final[2][1] and \
                    (self.board[0][2] == self.board[1][1] == self.board[2][0]) and \
                    (self.board[0][2] is not None):
                # game won diagonally right to left
                self.winner = self.board[0][2]
                return self.winner, ((0, 2), (2, 0))

        if self.turnNum > 9:
            self.winner = '-'
            return self.winner, None
        return None, None

    def place_x(self, row, col):
        """
        Places an X on the specified location, returns False if the move was unsuccessful and True if succesful
        """
        return self.place(row, col, 'x' + str(self.turnNum))

    def place_o(self, row, col):
        """
        Places an O on the specified location, returns False if the move was unsuccessful and True if succesful
        """
        return self.place(row, col, 'o' + str(self.turnNum))

    def place(self, row, col, char):
        if row > 2 or col > 2 or row < 0 or col < 0:
            return False
            # raise IndexError("Out of bounds")

        if self.final[row][col]:
            # todo: could return nice message that can be displayed in the UI
            return False

        # Check if the player does their two submoves on different tiles
        new_index = row * 3 + col
        if self.prevSubTurnIndex == new_index:
            return False

        self.board[row][col].append(char)
        if self.prevSubTurnIndex is not None:
            self.graph.add_edge(self.prevSubTurnIndex, new_index, char)
            self.prevSubTurnIndex = None

            # only need to do the check on the second sub-turn (end of turn)
            if self.subTurnNum % 2 == 1:
                cycle = self.graph.get_cycle(new_index)
                if cycle is not None:
                    tile_to_mark = resolve_superposition(self.board, self.graph, cycle, quantic=False)

                    # Mark all nodes in the cycle as final
                    for node_id in tile_to_mark.keys():
                        [row, col] = id_to_position(node_id)
                        self.final[row][col] = True

                    # Remove all edges and nodes that were in the cycle
                    self.graph.remove_cycle(cycle)

        return True


class GameState:
    def __init__(self):
        self.board = Board()
        self.reset()

    def x_moves(self):
        """
        Returns true if its X's turn to move
        """
        # return self.board.subTurnNum < 2
        return self.board.turnNum % 2 == 1

    def take_turn(self, row, col):
        if self.board.turnNum > 9 or self.board.winner is not None:
            return self.board.check_win()

        if self.x_moves():
            if not self.board.place_x(row, col):
                return False, None
        else:
            if not self.board.place_o(row, col):
                return False, None

        if self.board.subTurnNum == 1:
            self.board.turnNum += 1
        else:
            self.board.prevSubTurnIndex = row * 3 + col

        self.board.subTurnNum = (self.board.subTurnNum + 1) % 2

        return self.board.check_win()

    def reset(self):
        self.board.reset()
