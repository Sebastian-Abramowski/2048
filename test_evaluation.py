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
