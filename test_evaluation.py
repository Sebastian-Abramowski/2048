from board import Board


def test_get_max_number():
    board = Board([
        [8, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ], num_of_fields_in_row=4)
    assert board._get_max_value() == (128, False)


def test_get_max_number2():
    board = Board([
        [256, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ], num_of_fields_in_row=4)
    assert board._get_max_value() == (256, True)


def test_get_sum_of_values():
    board = Board([
        [8, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, None, None]
    ], num_of_fields_in_row=4)
    assert board._get_sum_of_values() == 259


def test_get_num_of_empty_fields():
    board = Board([
        [8, 4, 2, 1],
        [16, 32, 64, 128],
        [None, None, 2, 2],
        [None, None, 2, 2]
    ], num_of_fields_in_row=4)
    assert board._get_num_of_empty_fields() == 4


def test_evaluate_spreading_row():
    board = Board([
        [None, None, None, None],
        [None, None, None, None],
        [8, 4, 2, 2],
        [None, None, None, None]
    ], num_of_fields_in_row=4)
    assert board._evaluate_spreading() > 0

    board = Board([
        [8, 4, 2, 2],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ], num_of_fields_in_row=4)
    assert board._evaluate_spreading() > 0


def test_evaluate_spreading_column():
    board = Board([
        [None, None, None, 8],
        [None, None, None, 4],
        [None, None, None, 2],
        [None, None, None, 2]
    ], num_of_fields_in_row=4)
    assert board._evaluate_spreading() > 0

    board = Board([
        [16, None, None, None],
        [8, None, None, None],
        [4, None, None, None],
        [2, None, None, None]
    ], num_of_fields_in_row=4)
    assert board._evaluate_spreading() > 0


def test_evaluate_speading_diagonal():
    board = Board([
        [8, None, None, None],
        [None, 4, None, None],
        [None, None, 2, None],
        [None, None, None, 2]
    ], num_of_fields_in_row=4)
    assert board._evaluate_spreading() > 0


def test_count_blocked_fields_empty_board():
    board = Board([
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ], num_of_fields_in_row=4)

    board._get_num_of_blocked_fields_along_borders_without_corners() == 0
    board._get_num_of_blocked_fields_in_corners() == 0


def test_how_many_blocked_in_corners():
    board = Board([
        [128, 512, 128, 2],
        [256, 128, 64, 8],
        [16, 64, 32, 4],
        [2, 16, 8, 2]
    ], num_of_fields_in_row=4)
    assert board._get_num_of_blocked_fields_in_corners() == 4

    board = Board([
        [1024, 512, 128, 2],
        [256, None, 64, 8],
        [16, 64, None, 4],
        [8, 4, 8, 4]
    ], num_of_fields_in_row=4)
    assert board._get_num_of_blocked_fields_in_corners() == 1


def test_how_many_blocked_in_borders_without_corners_border_top():
    board = Board([
        [1024, 2, 4, 8],
        [None, 128, 64, None],
        [None, None, None, None],
        [None, None, None, None]
    ], num_of_fields_in_row=4)
    assert board._get_num_of_blocked_fields_along_borders_without_corners() == 1

    board = Board([
        [1024, 4, 2, 8],
        [None, 128, 64, None],
        [None, None, None, None],
        [None, None, None, None]
    ], num_of_fields_in_row=4)
    assert board._get_num_of_blocked_fields_along_borders_without_corners() == 1


def test_how_many_blocked_in_borders_without_corners_border_bottom():
    board = Board([
        [None, None, None, None],
        [None, None, None, None],
        [None, 64, 32, None],
        [16, 4, 8, 16]
    ], num_of_fields_in_row=4)
    board._get_num_of_blocked_fields_along_borders_without_corners() == 1

    board = Board([
        [None, None, None, None],
        [None, None, None, None],
        [None, 64, 32, None],
        [16, 8, 4, 16]
    ], num_of_fields_in_row=4)
    board._get_num_of_blocked_fields_along_borders_without_corners() == 1


def test_how_many_blocked_in_borders_without_corners_border_right():
    board = Board([
        [None, None, None, 64],
        [None, None, 64, 8],
        [None, None, 32, 4],
        [None, None, None, 64]
    ], num_of_fields_in_row=4)
    board._get_num_of_blocked_fields_along_borders_without_corners() == 1

    board = Board([
        [None, None, None, 64],
        [None, None, 64, 4],
        [None, None, 32, 8],
        [None, None, None, 64]
    ], num_of_fields_in_row=4)
    board._get_num_of_blocked_fields_along_borders_without_corners() == 1


def test_how_many_blocked_in_borders_without_corners_border_left():
    board = Board([
        [128, None, None, None],
        [2, 128, None, None],
        [32, 64, None, 4],
        [64, None, None, None]
    ], num_of_fields_in_row=4)
    board._get_num_of_blocked_fields_along_borders_without_corners() == 1

    board = Board([
        [128, None, None, None],
        [32, 128, None, None],
        [2, 64, None, 4],
        [64, None, None, None]
    ], num_of_fields_in_row=4)
    board._get_num_of_blocked_fields_along_borders_without_corners() == 1
