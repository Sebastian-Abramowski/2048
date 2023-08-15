import sys
import copy
from board import Board
from game import Game

sys.setrecursionlimit(5000)


def expectimax(board: Board, depth: int, max_player: bool, game: Game) -> tuple[int, str]:
    if depth == 0 or game.check_for_win(board) or game.check_if_blocked(board):
        return board.evaluate(), board

    if max_player:
        max_eval = float('-inf')
        best_direction = None
        for direction in ["up", "down", "left", "right"]:
            if game.check_if_able_to_move(board, direction):
                new_game = Game(copy.deepcopy(board))
                new_board = new_game.board
                new_game.move(direction, if_save_last_move=False)

                evaluation, _ = expectimax(new_board, depth - 1, False, game)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_direction = direction
        return max_eval, best_direction
    else:
        total_eval = 0
        empty_fields = board.get_empty_fields()

        for row_index, column_index in empty_fields:
            new_board_2 = copy.deepcopy(board)
            new_board_4 = copy.deepcopy(board)

            new_board_2.board_data[row_index][column_index] = 2
            eval_2, _ = expectimax(new_board_2, depth - 1, True, game)

            new_board_4.board_data[row_index][column_index] = 4
            eval_4, _ = expectimax(new_board_4, depth - 1, True, game)

            total_eval += 0.9 * eval_2 + 0.1 * eval_4

        if len(empty_fields) != 0:
            average_evaluation_value = total_eval / len(empty_fields)
        else:
            average_evaluation_value = 0

        return average_evaluation_value, None
