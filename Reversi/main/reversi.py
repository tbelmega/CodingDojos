"""
This is an implementation of the KataReversi <href>http://codingdojo.org/cgi-bin/index.pl?KataReversi</href>.
The task is to return a representation of all legal moves for a player in the Reversi game,
given a board situation and the color of the player.
"""
from copy import deepcopy

TIE = "Tie"

EMPTY_FIELD = '.'
BLACK = 'O'
WHITE = 'x'


def get_opponent(player):
    if player == BLACK:
        return WHITE
    else:
        return BLACK


class Field(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def equals(self, row, column):
        return self.row == row and self.column == column

    def __hash__(self):
        return self.row

    def __cmp__(self):
        return object.__cmp__(self)

    def __eq__(self, rhs):
        if isinstance(rhs, Field):
            return self.equals(rhs.row, rhs.column)
        else:
            return False

    def __str__(self):
        return '[' + str(self.row) + ',' + str(self.column) + ']'


class Board:
    def __init__(self):
        self.board = [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', BLACK, WHITE, '.', '.', '.'],
            ['.', '.', '.', WHITE, BLACK, '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        self.current_player = BLACK

    def pretty_print(self):
        Board.print_board(self.board)
        print "\n"

    def pretty_print_legal_moves(self, player):
        board_copy = deepcopy(self.board)
        for field in self.get_legal_moves(player):
            board_copy[field.row][field.column] = 'o'
        Board.print_board(board_copy)

    @staticmethod
    def print_board(board):
        for row in range(len(board)):
            row_string = ""
            for column in range(len(board[row])):
                row_string += board[row][column] + " "
            print row_string

    def rows(self):
        return len(self.board)

    def columns(self):
        return len(self.board[0])

    def get_field(self, field):
        return self.get(field.row, field.column)

    def get(self, row, column):
        return self.board[row][column]

    def get_legal_moves(self, player):
        self.current_player = player
        legal_moves = set()
        for row in range(self.rows()):
            for column in range(self.rows()):
                field = Field(row, column)
                if self.is_legal_move(field):
                    legal_moves.add(field)
        return legal_moves

    def is_legal_move(self, field):
        empty = self.board[field.row][field.column] == EMPTY_FIELD
        if not empty:
            return False
        else:
            return self.check_adjacent_fields(field)

    def check_adjacent_fields(self, field):
        """A 'legal constellation' is the combination of the param field,
        an adjacent field covered by a token of the opponent,
        and a field covered by the player right behind that.
        :param field: a Field on this board"""
        for vert in range(-1, 2):
            for hor in range(-1, 2):
                # check all combinations of vertical and horizontal deltas, apart from (0, 0)
                if not (vert == 0 and hor == 0):
                    if self.check_for_legal_constellation(field, vert, hor):
                        return True
        return False

    def check_for_legal_constellation(self, field, vert, hor):
        constellation_is_within_bounds = self.within_board_bounds(field.column, 2 * hor, field.row, 2 * vert)
        return constellation_is_within_bounds and self._legal_move_(field, vert, hor)

    def within_board_bounds(self, hor, look_hor, vert, look_vert):
        return vert + look_vert < self.rows() and hor + look_hor < self.columns()

    def _legal_move_(self, field, vert, hor):
        return self.adjacent_field_covered_by_opponent(field, vert, hor) \
               and self.field_behind_covered_by_player(field, vert, hor)

    def field_behind_covered_by_player(self, field, vert, hor):
        return self.get(field.row + 2 * vert, field.column + 2 * hor) == self.current_player

    def adjacent_field_covered_by_opponent(self, field, vert, hor):
        return self.get(field.row + 1 * vert, field.column + 1 * hor) == get_opponent(self.current_player)

    def perform_move(self, row, column):
        legal = self.is_legal_move(Field(row, column))
        if legal:
            self.place_token(row, column)
            self.current_player = get_opponent(self.current_player)
            return True
        else:
            return False

    def place_token(self, row, column):
        """Place own token on the specified field
        and look in all 8 directions for flippable opponent's tokens."""
        self.board[row][column] = self.current_player
        for vert in range(-1, 2):
            for hor in range(-1, 2):
                # check all combinations of vertical and horizontal deltas, apart from (0, 0)
                if not (vert == 0 and hor == 0):
                    self.flip(row, column, vert, hor)

    def flip(self, row, column, look_vert, look_hor):
        if self.within_board_bounds(column, look_hor, row, look_vert):
            if self.is_flippable(column, look_hor, row, look_vert):
                self.board[row + look_vert][column + look_hor] = self.current_player
                self.flip(row + look_vert, column + look_hor, look_vert, look_hor)

    def is_flippable(self, hor, look_hor, vert, look_vert):
        return self.board[vert + look_vert][hor + look_hor] == get_opponent(self.current_player)

    def count(self, player):
        count = 0
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.get(row, column) == player:
                    count += 1
        return count

    def predict_flips(self, row, column):
        prediction = 0
        for vert in range(-1, 2):
            for hor in range(-1, 2):
                if not (vert == 0 and hor == 0):
                    prediction += self.predict_flips_in_direction(row, column, vert, hor)
        return prediction

    def predict_flips_in_direction(self, row, column, look_vert, look_hor):
        if self.within_board_bounds(column, look_hor, row, look_vert):
            if self.is_flippable(column, look_hor, row, look_vert):
                return 1 + self.predict_flips_in_direction(row + look_vert, column + look_hor, look_vert, look_hor)
        return 0

    def find_best_legal_move(self):
        best_prediction = 0
        best_move = None
        for move in self.get_legal_moves(self.current_player):
            prediction = self.predict_flips(move.row, move.column)
            if prediction > best_prediction:
                best_move = move
                best_prediction = prediction
        return best_move

    def ai_move(self):
        move = self.find_best_legal_move()
        if move is None:
            return self.winning_player()
        self.perform_move(move.row, move.column)
        print ""
        self.pretty_print()

    def winning_player(self):
        black = self.count(BLACK)
        white = self.count(WHITE)
        if black > white:
            return BLACK
        elif white > black:
            return WHITE
        else:
            return TIE


def main():
    board = Board()
    winner = None
    while winner is None:
        winner = board.ai_move()
        legal = board.get_legal_moves(board.current_player)
        if not legal:
            winner = board.winning_player()
        else:
            moved = False
            while not moved:
                print "Your move"
                row = int(raw_input('row: '))
                column = int(raw_input('column: '))
                moved = board.perform_move(row, column)
                if not moved:
                    print("That move is not legal, try again.\n")
            board.pretty_print()
    print "\n"
    print "Game over! The winner is " + winner + "!"


if __name__ == "__main__":
    main()
