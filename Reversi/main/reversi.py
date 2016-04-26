"""
This is an implementation of the KataReversi <href>http://codingdojo.org/cgi-bin/index.pl?KataReversi</href>.
The task is to return a representation of all legal moves for a player in the Reversi game,
given a board situation and the color of the player.
"""

EMPTY_FIELD = '.'
BLACK = 'B'
WHITE = 'W'


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
            ['.', '.', '.', 'B', 'W', '.', '.', '.'],
            ['.', '.', '.', 'W', 'B', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ]
        self.current_player = ""

    def pretty_print(self):
        for row in range(len(self.board)):
            row_string = ""
            for column in range(len(self.board[row])):
                row_string += self.get(row, column)
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
        """A 'legal constellation' is the combination of the param field,
        an adjacent field covered by a token of the opponent,
        and a field covered by the player right behind that.
        :param field: a Field on this board"""
        above = self.check_for_legal_constellation(field, -1, 0)
        below = self.check_for_legal_constellation(field, 1, 0)
        on_the_left = self.check_for_legal_constellation(field, 0, -1)
        on_the_right = self.check_for_legal_constellation(field, 0, 1)
        return above or below or on_the_left or on_the_right

    def check_for_legal_constellation(self, field, vert, hor):
        constellation_is_within_bounds = self.within_board_bounds(field, vert, hor)
        return constellation_is_within_bounds and self._legal_move_(field, vert, hor)

    def _legal_move_(self, field, vert, hor):
        return self.adjacent_field_covered_by_opponent(field, vert, hor) \
               and self.field_behind_covered_by_player(field, vert, hor)

    def field_behind_covered_by_player(self, field, vert, hor):
        return self.get(field.row + 2 * vert, field.column + 2 * hor) == self.current_player

    def adjacent_field_covered_by_opponent(self, field, vert, hor):
        return self.get(field.row + 1 * vert, field.column + 1 * hor) == get_opponent(self.current_player)

    def within_board_bounds(self, field, vert, hor):
        return field.row + 2 * vert < self.rows() and field.column + 2 * hor < self.columns()
