import unittest

from main import reversi
from main.reversi import Board, Field


def is_white_start_position(field):
    """Initially place white tokens on [3][4] and [4][3]"""
    return field.equals(3, 4) or field.equals(4, 3)


def is_black_start_position(field):
    """Initially place black tokens on [3][3] and [4][4]"""
    return field.equals(3, 3) or field.equals(4, 4)


class ReversiTest(unittest.TestCase):
    def testThatFieldHasRow(self):
        field = Field(1, 4)
        self.assertEquals(1, field.row)

    def testThatFieldHasColumn(self):
        field = Field(1, 4)
        self.assertEquals(4, field.column)

    def testThatFieldEqualsReturnsTrueOnOwnCoordinates(self):
        field = Field(1, 4)
        self.assertTrue(field.equals(1, 4))

    def testThatFieldEqualsReturnsFalseOnOtherCoordinates(self):
        field = Field(1, 4)
        self.assertFalse(field.equals(1, 5))

    def testThatBoardHas8Rows(self):
        board = Board()
        self.assertEquals(8, board.rows(), "Reversi board should have 8 rows, but has " + str(board.rows()))

    def testThatBoardHas8Columns(self):
        board = Board()
        self.assertEquals(8, board.columns(), "Reversi board should have 8 columns, but has " + str(board.columns()))

    def testThatFirstFourTokensArePlaced(self):
        """Assert that initial token placement matches specification,
        see <href>http://codingdojo.org/cgi-bin/index.pl?KataReversi</href> """
        board = Board()
        for row in range(board.rows()):
            for column in range(board.rows()):
                field = Field(row, column)
                if is_white_start_position(field):
                    self.assertEquals(reversi.WHITE, board.get_field(field))
                elif is_black_start_position(field):
                    self.assertEquals(reversi.BLACK, board.get_field(field))
                else:
                    self.assertEquals(reversi.EMPTY_FIELD, board.get_field(field))

    def testThatInitialBoardContainsLegalMove24(self):
        board = Board()
        board.current_player = reversi.BLACK
        legal = board.is_legal_move(Field(2, 4))
        self.assertTrue(legal)

    def testThatInitialBoardContainsLegalMove35(self):
        board = Board()
        board.current_player = reversi.BLACK
        legal = board.is_legal_move(Field(3, 5))
        self.assertTrue(legal)

    def testThatInitialBoardContainsLegalMove42(self):
        board = Board()
        board.current_player = reversi.BLACK
        legal = board.is_legal_move(Field(4, 2))
        self.assertTrue(legal)

    def testThatInitialBoardContainsLegalMove53(self):
        board = Board()
        board.current_player = reversi.BLACK
        legal = board.is_legal_move(Field(5, 3))
        self.assertTrue(legal)

    def testThatInitialBoardReturnsExpectedLegalMovesForBlack(self):
        expected_legal_moves = [Field(2, 4), Field(3, 5), Field(4, 2), Field(5, 3)]
        legal_moves = Board().get_legal_moves(reversi.BLACK)
        self.assertSetEqual(set(expected_legal_moves), legal_moves)

    def testThatInitialBoardReturnsExpectedLegalMovesForWhite(self):
        expected_legal_moves = [Field(2, 3), Field(3, 2), Field(4, 5), Field(5, 4)]
        legal_moves = Board().get_legal_moves(reversi.WHITE)
        self.assertSetEqual(set(expected_legal_moves), legal_moves)

    def testThatDiagonalMovesToUpperRightAreLegal(self):
        board = Board()
        board.board[4][3] = reversi.BLACK
        self.assertTrue(board.is_legal_move(Field(2, 5)))

    def testThatDiagonalMovesToLowerLeftAreLegal(self):
        board = Board()
        board.board[3][4] = reversi.BLACK
        self.assertTrue(board.is_legal_move(Field(5, 2)))

    def testThatDiagonalMovesToUpperLeftAreLegal(self):
        board = Board()
        board.board[3][3] = reversi.WHITE
        self.assertTrue(board.is_legal_move(Field(2, 2)))

    def testThatDiagonalMovesToLowerRightAreLegal(self):
        board = Board()
        board.board[4][4] = reversi.WHITE
        self.assertTrue(board.is_legal_move(Field(5, 5)))

    def testThatPerformLegalMoveReturnsTrue(self):
        board = Board()
        performed = board.perform_move(2, 4)
        self.assertTrue(performed)

    def testThatAfterMoveCurrentPlayerChanged(self):
        board = Board()
        board.perform_move(2, 4)
        self.assertEquals(reversi.WHITE, board.current_player)

    def testThatIllegalMoveIsRefused(self):
        board = Board()
        performed = board.perform_move(2, 3)
        self.assertFalse(performed)
        self.assertEquals(reversi.BLACK, board.current_player)

    def testThatAfterMoveTheFieldContainsToken(self):
        board = Board()
        board.perform_move(2, 4)
        self.assertEquals(reversi.BLACK, board.get(2, 4))

    def testThatAfterMoveOpponentsTokenIsTurned(self):
        board = Board()
        board.perform_move(2, 4)
        self.assertEquals(reversi.BLACK, board.get(3, 4))

    def testThatAfterMoveMultipleTokensAreTurned(self):
        # ARRANGE
        board = Board()
        board.board[2][4] = reversi.WHITE
        board.board[2][5] = reversi.WHITE
        board.board[1][3] = reversi.WHITE
        board.board[1][2] = reversi.BLACK
        # ACT
        board.perform_move(1, 4)
        # ASSERT
        board.pretty_print()
        self.assertEquals(reversi.BLACK, board.get(1, 3))
        self.assertEquals(reversi.BLACK, board.get(2, 4))
        self.assertEquals(reversi.WHITE, board.get(2, 5))
        self.assertEquals(reversi.BLACK, board.get(3, 4))

    def testThatTokensOnBoardAreCounted(self):
        board = Board()
        board.perform_move(2, 4)
        self.assertEquals(4, board.count(reversi.BLACK))
        self.assertEquals(1, board.count(reversi.WHITE))

    def testThatBoardPredictsNumberOfFlips(self):
        board = Board()
        flips = board.predict_flips(4, 2)
        self.assertEquals(1, flips)

    def testThatBestLegalMoveIsFound(self):
        # ARRANGE
        board = Board()
        board.board[2][4] = reversi.WHITE
        board.board[1][3] = reversi.WHITE
        board.board[1][2] = reversi.BLACK
        board.board[2][5] = reversi.BLACK
        board.current_player = reversi.BLACK
        move = board.find_best_legal_move()
        self.assertEquals(Field(1, 4), move)

    # def testAiGame(self):
    #     board = Board()
    #     winner = None
    #     while winner is None:
    #         winner = board.ai_move()
    #     print("\nWinner: " + winner)
    #     self.assertTrue(winner == reversi.BLACK or winner == reversi.WHITE)

