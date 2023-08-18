import matplotlib.pyplot as plt
from pathlib import Path
from typing import Union
from collections import deque
from board import Board
from game import Game
from expectimax import expectimax


def configurate_plot(x_title: str, y_title: str, title: str) -> None:
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.style.use("fivethirtyeight")
    plt.grid(True)


def show_plot() -> None:
    plt.legend()
    plt.show()


def save_plot(file_path: Union[Path, str]) -> None:
    plt.legend()
    plt.savefig(file_path)


def clear_after_making_the_plot() -> None:
    plt.cla()
    plt.style.use("default")


def make_plot(plot_data: dict[int, dict]) -> None:
    """
    Example of plot_data:
    plot_data = {4: {"number_of_game": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     "scores": [10, 192, 194, 3000, 234, 1243, 4352, 2345, 2345, 10923]},
                 5: {"number_of_game": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     "scores": [25, 234, 235, 4021, 20, 1245, 353, 3245, 9895, 10432]}}
    """

    configurate_plot("Nth game",
                     "Score",
                     "Scores got in N games with Expectimax algorithm with given depth")

    stack_with_colors = deque(['#8bd3c7', '#fdcce5', '#beb9db',
                               '#ffee65', '#ffb55a', '#bd7ebe',
                               '#b2e061', '#7eb0d5', '#fd7f6f'])

    for depth, data_for_single_plot in plot_data.items():
        plt.plot(data_for_single_plot["number_of_game"],
                 data_for_single_plot["scores"],
                 label=f"depth: {depth}", color=stack_with_colors.pop())


def make_data_for_plot(depths: list, number_of_games: int) -> dict[int, dict]:
    data_for_plot = dict()

    for depth in depths:
        single_plot_data = dict()
        single_plot_data["number_of_game"] = range(1, number_of_games + 1)

        scores = []
        for _ in range(number_of_games):
            board = Board(game_start=True)
            game = Game(board)
            print(game.score)

            run = True
            while run:
                if Game.check_if_blocked(game.board):
                    scores.append(game.score)
                    run = False
                    continue

                _, best_direction = expectimax(game.board, depth, True)
                if best_direction:
                    game.move(best_direction, if_save_last_move=False)
                    game.board.add_new_random_field()

        single_plot_data["scores"] = scores
        data_for_plot[depth] = single_plot_data

    return data_for_plot


def main():
    plot_data = make_data_for_plot([2, 3, 4, 5], 10)
    make_plot(plot_data)
    show_plot()
    clear_after_making_the_plot()


if __name__ == "__main__":
    main()
