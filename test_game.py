import numpy as np
from board import Board
from game import Game
import utilities
import pytest

# TEST MOVING RIGHT


def test_move_right_without_none_between():
    board = Board([[None] * 4,
                   [None] * 4,
                   [None] * 4,
                   [2, 2, 2, 2]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [None] * 4,
        [None, None, 4, 4]
    ])


def test_move_right_with_none_between():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, None, 2, None],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [None, None, None, 4],
        [None] * 4
    ])


def test_just_move_right():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, 2, None],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [None, 2, 8, 2],
        [None] * 4
    ])


def test_move_right_blocked():
    starting_board = [[None] * 4,
                      [None] * 4,
                      [2, 8, 4, 2],
                      [None] * 4]
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, 4, 2],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert not game.move("right")
    assert np.array_equal(board.board_data, starting_board)


def test_move_right_partially_blocked():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, None, 8, 2],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [None, 2, 8, 2],
        [None] * 4]
    )


def test_move_right_double_merging():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 2, 4, 4],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [None, None, 4, 8],
        [None] * 4]
    )


def test_move_right_ultimate_test():
    board = Board(
        [[2, None, None, None, None, 2],
         [2, 2, 4, 4, 2, 2],
         [2, 4, 8, 16, 32, None],
         [2, 4, 8, 16, 32, 64],
         [2, 2, None, None, 16, 16],
         [None, 2, 2, None, 4, None]],
        num_of_fields_in_row=6,
    )
    game = Game(board, num_of_fields_in_row=6)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None, None, None, None, None, 4],
        [None, None, None, 4, 8, 4],
        [None, 2, 4, 8, 16, 32],
        [2, 4, 8, 16, 32, 64],
        [None, None, None, None, 4, 32],
        [None, None, None, None, 4, 4]]
    )


def test_move_right_order():
    board = Board([[None] * 4,
                   [None] * 4,
                   [None, 2, 2, 2],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("right")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [None, None, 2, 4],
        [None] * 4]
    )


# TEST MOVING LEFT


def test_move_left_without_none_between():
    board = Board([[None] * 4,
                   [4, None, None, None],
                   [None, None, None, 4],
                   [2, 2, 2, 2]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [4, None, None, None],
        [4, None, None, None],
        [4, 4, None, None]]
    )


def test_move_left_with_none_between():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, None, 2, None],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [4, None, None, None],
        [None] * 4]
    )


def test_just_move_left():
    board = Board([[None] * 4,
                   [None] * 4,
                   [None, 8, 2, 4],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [8, 2, 4, None],
        [None] * 4]
    )


def test_move_left_blocked():
    starting_board = [[None] * 4,
                      [None] * 4,
                      [2, 8, 4, 2],
                      [None] * 4]
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, 4, 2],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert not game.move("left")
    assert np.array_equal(board.board_data, starting_board)


def test_move_left_partially_blocked():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 8, None, 2],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [2, 8, 2, None],
        [None] * 4]
    )


def test_move_left_double_merging():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 2, 4, 4],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [4, 8, None, None],
        [None] * 4]
    )


def test_move_left_ultimate_test():
    board = Board(
        [[2, None, None, None, None, 2],
         [2, 2, 4, 4, 2, 2],
         [None, 2, 4, 8, 16, 32],
         [2, 4, 8, 16, 32, 64],
         [2, 2, None, None, 16, 16],
         [None, 2, 2, None, 4, None]],
        num_of_fields_in_row=6,
    )
    game = Game(board, num_of_fields_in_row=6)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [4, None, None, None, None, None],
        [4, 8, 4, None, None, None],
        [2, 4, 8, 16, 32, None],
        [2, 4, 8, 16, 32, 64],
        [4, 32, None, None, None, None],
        [4, 4, None, None, None, None]]
    )


def test_move_left_order():
    board = Board([[None] * 4,
                   [None] * 4,
                   [2, 2, 2, None],
                   [None] * 4], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("left")
    assert np.array_equal(board.board_data, [
        [None] * 4,
        [None] * 4,
        [4, 2, None, None],
        [None] * 4]
    )


# TEST MOVING UP


def test_move_up_without_none_between():
    board = Board([[None, 2, None, None],
                   [None, 2, None, None],
                   [None, 2, None, None],
                   [None, 2, None, None]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [None, 4, None, None],
        [None, 4, None, None],
        [None, None, None, None],
        [None, None, None, None]]
    )


def test_move_up_with_none_between():
    board = Board([[None, None, None, 4],
                   [2, None, None, None],
                   [None, None, None, None],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [4, None, None, 8],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]]
    )


def test_just_move_up():
    board = Board([[None, None, None, 16],
                   [None, None, None, None],
                   [4, None, None, None],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [4, None, None, 16],
        [2, None, None, 4],
        [None, None, None, None],
        [None, None, None, None]]
    )


def test_move_up_blocked():
    starting_board = [[16, None, None, 16],
                      [8, None, None, 2],
                      [4, None, None, 8],
                      [2, None, None, 4]]
    board = Board([[16, None, None, 16],
                   [8, None, None, 2],
                   [4, None, None, 8],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert not game.move("up")
    assert np.array_equal(board.board_data, starting_board)


def test_move_up_partially_blocked():
    board = Board([[2, None, None, 16],
                   [None, None, None, 2],
                   [8, None, None, None],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [2, None, None, 16],
        [8, None, None, 2],
        [2, None, None, 4],
        [None, None, None, None]]
    )


def test_move_up_double_merging():
    board = Board([[2, None, None, 2],
                   [2, None, None, 2],
                   [4, None, None, 2],
                   [4, None, None, 2]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [4, None, None, 4],
        [8, None, None, 4],
        [None, None, None, None],
        [None, None, None, None]]
    )


def test_move_up_ultimate_test():
    board = Board(
        [[2, 2, 64, None, 2, 2],
         [None, 2, 2, 2, 2, None],
         [None, 4, 4, 4, None, None],
         [None, 4, 8, 8, None, None],
         [None, 2, 16, 16, 16, None],
         [2, 2, 32, 32, 32, 16]], num_of_fields_in_row=6
    )
    game = Game(board, num_of_fields_in_row=6)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [4, 4, 64, 2, 4, 2],
        [None, 8, 2, 4, 16, 16],
        [None, 4, 4, 8, 32, None],
        [None, None, 8, 16, None, None],
        [None, None, 16, 32, None, None],
        [None, None, 32, None, None, None]]
    )


def test_move_up_order():
    board = Board([[2, None, None, None],
                   [2, None, None, 4],
                   [2, None, None, 4],
                   [None, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("up")
    assert np.array_equal(board.board_data, [
        [4, None, None, 8],
        [2, None, None, 4],
        [None, None, None, None],
        [None, None, None, None]]
    )


# TEST MOVING DOWN


def test_move_down_without_none_between():
    board = Board([[None, 2, None, None],
                   [None, 2, None, None],
                   [None, 2, None, None],
                   [None, 2, None, None]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, None, None],
        [None, None, None, None],
        [None, 4, None, None],
        [None, 4, None, None]]
    )


def test_move_down_with_none_between():
    board = Board([[None, None, None, 4],
                   [2, None, None, None],
                   [None, None, None, None],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [4, None, None, 8]]
    )


def test_just_move_down():
    board = Board([[4, None, None, 16],
                   [2, None, None, None],
                   [None, None, None, None],
                   [None, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, None, None],
        [None, None, None, None],
        [4, None, None, 16],
        [2, None, None, 4]]
    )


def test_move_down_blocked():
    starting_board = [[16, None, None, 16],
                      [8, None, None, 2],
                      [4, None, None, 8],
                      [2, None, None, 4]]
    board = Board([[16, None, None, 16],
                   [8, None, None, 2],
                   [4, None, None, 8],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert not game.move("down")
    assert np.array_equal(board.board_data, starting_board)


def test_move_down_partially_blocked():
    board = Board([[2, None, None, 16],
                   [None, None, None, 2],
                   [8, None, None, None],
                   [2, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, None, None],
        [2, None, None, 16],
        [8, None, None, 2],
        [2, None, None, 4]]
    )


def test_move_down_double_merging():
    board = Board([[2, None, None, 2],
                   [2, None, None, 2],
                   [4, None, None, 2],
                   [4, None, None, 2]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, None, None],
        [None, None, None, None],
        [4, None, None, 4],
        [8, None, None, 4]]
    )


def test_move_down_ultimate_test():
    board = Board(
        [[2, 2, 64, 2, 2, 2],
         [None, 2, 2, 4, 2, None],
         [None, 4, 4, 8, None, None],
         [None, 4, 8, 16, None, None],
         [None, 2, 16, 32, 16, None],
         [2, 2, 32, 32, None, 16]], num_of_fields_in_row=6
    )
    game = Game(board, num_of_fields_in_row=6)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, 64, None, None, None],
        [None, None, 2, 2, None, None],
        [None, None, 4, 4, None, None],
        [None, 4, 8, 8, None, None],
        [None, 8, 16, 16, 4, 2],
        [4, 4, 32, 64, 16, 16]]
    )


def test_move_down_order():
    board = Board([[2, None, None, None],
                   [2, None, None, 4],
                   [2, None, None, 4],
                   [None, None, None, 4]], num_of_fields_in_row=4)
    game = Game(board, num_of_fields_in_row=4)

    assert game.move("down")
    assert np.array_equal(board.board_data, [
        [None, None, None, None],
        [None, None, None, None],
        [2, None, None, 4],
        [4, None, None, 8]]
    )


# --------------------------------------------------------


def test_static_check_for_win():
    board = Board([[2, None, None, None],
                   [2, None, None, 4],
                   [2, None, None, 4],
                   [None, None, None, 4]], num_of_fields_in_row=4)

    board2 = Board([[2, None, None, None],
                   [2, None, 2048, 4],
                   [2, None, None, 4],
                   [None, None, None, 4]], num_of_fields_in_row=4)

    assert not Game.check_for_win(board)
    assert Game.check_for_win(board2)


def test_static_check_if_blocked():
    board = Board([[2, None, None, None],
                   [2, None, None, 4],
                   [2, None, None, 4],
                   [None, None, None, 4]], num_of_fields_in_row=4)
    assert not Game.check_if_blocked(board, num_of_fields_in_single_row=4)

    board = Board([[16, 2, 64, 16],
                   [8, 4, 32, 2],
                   [4, 8, 16, 8],
                   [2, 16, 8, 4]], num_of_fields_in_row=4)
    assert Game.check_if_blocked(board, num_of_fields_in_single_row=4)


def test_static_check_if_able_to_move():
    board = Board([[2, None, None, None],
                   [2, None, None, 4],
                   [2, None, None, 4],
                   [None, None, None, 4]], num_of_fields_in_row=4)
    if_sth_changed, changed_board = Game.check_if_able_to_move(board, "up",
                                                               num_of_fields_in_single_row=4)
    assert if_sth_changed
    assert np.array_equal(changed_board.board_data, [
        [4, None, None, 8],
        [2, None, None, 4],
        [None, None, None, None],
        [None, None, None, None]]
    )

    board = Board([[16, 2, 64, 16],
                   [8, 4, 32, 2],
                   [4, 8, 16, 8],
                   [2, 16, 8, 4]], num_of_fields_in_row=4)
    if_sth_changed, changed_board = Game.check_if_able_to_move(board, "up",
                                                               num_of_fields_in_single_row=4)
    assert not if_sth_changed
    assert np.array_equal(changed_board.board_data, board.board_data)

    if_sth_changed, changed_board = Game.check_if_able_to_move(board, "down",
                                                               num_of_fields_in_single_row=4)
    assert not if_sth_changed
    assert np.array_equal(changed_board.board_data, board.board_data)

    if_sth_changed, changed_board = Game.check_if_able_to_move(board, "right",
                                                               num_of_fields_in_single_row=4)
    assert not if_sth_changed
    assert np.array_equal(changed_board.board_data, board.board_data)

    if_sth_changed, changed_board = Game.check_if_able_to_move(board, "left",
                                                               num_of_fields_in_single_row=4)
    assert not if_sth_changed
    assert np.array_equal(changed_board.board_data, board.board_data)


def test_direction_validation_no_error():
    board = Board()
    game = Game(board)

    # no error
    game._validate_function_with_direction("right")
    game._validate_function_with_direction("left")
    game._validate_function_with_direction("up")
    game._validate_function_with_direction("down")


def test_direction_validation_error():
    board = Board()
    game = Game(board)

    # error
    with pytest.raises(utilities.WrongUseOfFuncionError):
        game._validate_function_with_direction("diagonal")
    with pytest.raises(utilities.WrongUseOfFuncionError):
        game._validate_function_with_direction("top")
    with pytest.raises(utilities.WrongUseOfFuncionError):
        game._validate_function_with_direction("bottom")
