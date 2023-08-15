import copy
import numpy as np
import random
from board import Board


def test_get_empty_fields():
    board = Board([
        [8, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ], num_of_fields_in_row=4)

    empty_fields = board.get_empty_fields()
    assert empty_fields == [(2, 0), (2, 1), (3, 0), (3, 1)]


def test_board_deepcopy():
    board = Board([
        [8, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ], num_of_fields_in_row=4)
    board_copied = copy.deepcopy(board)

    assert board_copied.num_of_fields_in_row == 4

    board.board_data[0][0] = 64

    assert np.array_equal(board.board_data, [
        [64, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ])
    assert np.array_equal(board_copied.board_data, [
        [8, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ])
    assert not np.array_equal(board.board_data, board_copied.board_data)


def test_board_init():
    board = Board(num_of_fields_in_row=4)
    num_of_not_empty_fields = np.count_nonzero(np.logical_or(board.board_data == 2, board.board_data == 4))
    assert num_of_not_empty_fields == 0


def test_board_init2():
    board = Board(game_start=True, num_of_fields_in_row=4)
    num_of_not_empty_fields = np.count_nonzero(np.logical_or(board.board_data == 2, board.board_data == 4))
    assert num_of_not_empty_fields == 2


def test_get_empty_board():
    board = Board(num_of_fields_in_row=4)

    assert board._get_empty_board() == [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    assert np.array_equal(board.board_data, board._get_empty_board())

    board = Board(num_of_fields_in_row=6)

    assert board._get_empty_board() == [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
    ]
    assert np.array_equal(board.board_data, board._get_empty_board())


def test_add_new_random_fields(monkeypatch):
    board = Board(num_of_fields_in_row=4)

    def get_random_fields(*args):
        return (0, 2)

    def get_random_number(arg, arg2, k):
        return [2]

    monkeypatch.setattr(random, "choice", get_random_fields)
    monkeypatch.setattr(random, "choices", get_random_number)

    assert board.add_new_random_field()
    assert np.count_nonzero(board.board_data == 2) == 1
    assert np.count_nonzero(board.board_data == None) == 15
    assert board.board_data[0][2] == 2
