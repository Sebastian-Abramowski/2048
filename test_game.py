from board import Board
from game import Game

# TEST MOVING RIGHT


def test_move_right_without_none_between():
    board = Board([[None]*4, [None]*4, [None]*4, [2, 2, 2, 2]])
    game = Game(board)
    game.move_right()
    print(board)
    assert board.board_data == [[None]*4, [None]*4,
                                [None]*4, [None, None, 4, 4]]


def test_move_right_with_none_between():
    board = Board([[None]*4, [None]*4, [2, None, 2, None], [None]*4])
    game = Game(board)
    game.move_right()
    assert board.board_data == [[None]*4, [None]*4, [None, None, None, 4], [None]*4]


def test_just_move_right():
    board = Board([[None]*4, [None]*4, [2, 8, 2, None], [None]*4])
    game = Game(board)
    game.move_right()
    assert board.board_data == [[None]*4, [None]*4, [None, 2, 8, 2], [None]*4]


def test_move_right_blocked():
    starting_board = [[None]*4, [None]*4, [2, 8, 4, 2], [None]*4]
    board = Board([[None]*4, [None]*4, [2, 8, 4, 2], [None]*4])
    game = Game(board)
    game.move_right()
    assert board.board_data == starting_board


def test_move_right_partially_blocked():
    board = Board([[None]*4, [None]*4, [2, None, 8, 2], [None]*4])
    game = Game(board)
    game.move_right()
    assert board.board_data == [[None]*4, [None]*4, [None, 2, 8, 2], [None]*4]


def test_move_right_partially_blocked2():
    board = Board([[None]*4, [None]*4, [2, 2, 4, 4], [None]*4])
    game = Game(board)
    game.move_right()
    assert board.board_data == [[None]*4, [None]*4, [None, None, 4, 8], [None]*4]


def test_move_right_ultimate_test():
    pass
