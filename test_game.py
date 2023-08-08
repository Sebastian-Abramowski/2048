from board import Board
from game import Game

# TEST MOVING RIGHT


def test_move_right_without_none_between():
    board = Board([[None] * 4,
                   [None] * 4,
                   [None] * 4,
                   [2, 2, 2, 2]])
    game = Game(board)
    assert game.move_horiziontally("right") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [None] * 4,
                                [None, None, 4, 4]]


def test_move_right_with_none_between():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, None, 2, None],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("right") is True
    assert board.board_data == [
        [None] * 4,
        [None] * 4,
        [None, None, None, 4],
        [None] * 4,
    ]


def test_just_move_right():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, 2, None],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("right") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [None, 2, 8, 2],
                                [None] * 4]


def test_move_right_blocked():
    starting_board = [[None] * 4,
                      [None] * 4,
                      [2, 8, 4, 2],
                      [None] * 4]
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, 4, 2],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("right") is False
    assert board.board_data == starting_board


def test_move_right_partially_blocked():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, None, 8, 2],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("right") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [None, 2, 8, 2],
                                [None] * 4]


def test_move_right_partially_blocked2():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 2, 4, 4],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("right") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [None, None, 4, 8],
                                [None] * 4]


def test_move_right_ultimate_test():
    board = Board(
        [
            [2, None, None, None, None, 2],
            [2, 2, 4, 4, 2, 2],
            [2, 4, 8, 16, 32, None],
            [2, 4, 8, 16, 32, 64],
            [2, 2, None, None, 16, 16],
            [None, 2, 2, None, 4, None],
        ],
        num_of_fields_in_row=6,
    )
    game = Game(board, num_of_fields_in_row=6)
    assert game.move_horiziontally("right") is True
    assert board.board_data == [
        [None, None, None, None, None, 4],
        [None, None, None, 4, 8, 4],
        [None, 2, 4, 8, 16, 32],
        [2, 4, 8, 16, 32, 64],
        [None, None, None, None, 4, 32],
        [None, None, None, None, 4, 4]]


# TEST MOVING LEFT


def test_move_left_without_none_between():
    board = Board([[None] * 4,
                   [4, None, None, None],
                   [None, None, None, 4],
                   [2, 2, 2, 2]])
    game = Game(board)
    assert game.move_horiziontally("left") is True
    assert board.board_data == [[None] * 4,
                                [4, None, None, None],
                                [4, None, None, None],
                                [4, 4, None, None]]


def test_move_left_with_none_between():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, None, 2, None],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("left") is True
    assert board.board_data == [
        [None] * 4,
        [None] * 4,
        [4, None, None, None],
        [None] * 4]


def test_just_move_left():
    board = Board([[None] * 4,
                   [None] * 4,
                   [None, 8, 2, 4],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("left") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [8, 2, 4, None],
                                [None] * 4]


def test_move_left_blocked():
    starting_board = [[None] * 4,
                      [None] * 4,
                      [2, 8, 4, 2],
                      [None] * 4]
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, 4, 2],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("left") is False
    assert board.board_data == starting_board


def test_move_left_partially_blocked():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, None, 2],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("left") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [2, 8, 2, None],
                                [None] * 4]


def test_move_left_partially_blocked2():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 2, 4, 4],
                   [None] * 4])
    game = Game(board)
    assert game.move_horiziontally("left") is True
    assert board.board_data == [[None] * 4,
                                [None] * 4,
                                [4, 8, None, None],
                                [None] * 4]


def test_move_left_ultimate_test():
    board = Board(
        [
            [2, None, None, None, None, 2],
            [2, 2, 4, 4, 2, 2],
            [None, 2, 4, 8, 16, 32],
            [2, 4, 8, 16, 32, 64],
            [2, 2, None, None, 16, 16],
            [None, 2, 2, None, 4, None],
        ],
        num_of_fields_in_row=6,
    )
    game = Game(board, num_of_fields_in_row=6)
    assert game.move_horiziontally("left") is True
    assert board.board_data == [
        [4, None, None, None, None, None],
        [4, 8, 4, None, None, None],
        [2, 4, 8, 16, 32, None],
        [2, 4, 8, 16, 32, 64],
        [4, 32, None, None, None, None],
        [4, 4, None, None, None, None]]
