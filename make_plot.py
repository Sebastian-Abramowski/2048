import matplotlib.pyplot as plt
from pathlib import Path
from typing import Union
from collections import deque
from board import Board
from game import Game
from expectimax import expectimax
from tqdm import tqdm


def configurate_plot(x_title: str, y_title: str, title: str) -> None:
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.style.use("fivethirtyeight")
    plt.grid(True)


def show_legend() -> None:
    plt.legend()


def show_plot() -> None:
    plt.show()


def save_plot(file_path: Union[Path, str]) -> None:
    plt.savefig(file_path)


def clear_after_making_plot() -> None:
    plt.cla()
    plt.style.use("default")


def make_plot_with_scores(plot_data: dict[int, dict]) -> None:
    """
    Example of plot_data:
    plot_data = {4: {"number_of_game": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     "scores": [10, 192, 194, 3000, 234, 1243, 4352, 2345, 2345, 10923]},
                 5: {"number_of_game": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     "scores": [25, 234, 235, 4021, 20, 1245, 353, 3245, 9895, 10432]}}

    Keys are depths
    Dictionaries should have the same number of games
    """
    configurate_plot("Nth game",
                     "Score",
                     "Scores got in N games with Expectimax algorithm with given depth")

    stack_with_colors = deque(['#8bd3c7', '#fdcce5', '#beb9db',
                               '#ffee65', '#ffb55a', '#bd7ebe',
                               '#b2e061', '#7eb0d5', '#fd7f6f'])

    values_on_x_axis = None
    for depth, data_for_single_plot in plot_data.items():
        if not values_on_x_axis:
            values_on_x_axis = data_for_single_plot["number_of_game"]
        plt.plot(data_for_single_plot["number_of_game"],
                 data_for_single_plot["scores"],
                 label=f"depth: {depth}", color=stack_with_colors.pop())
    plt.xticks(values_on_x_axis)
    # update title with number of games
    plt.title(f"Scores got in {len(values_on_x_axis)} games with Expectimax algorithm with given depth",
              fontsize=12)


def make_plot_with_wins(plot_data: dict[int, int], number_of_games: int) -> None:
    """
    Example of plot_data
    plot_data = {1: 0, 2: 23, 3: 34}

    Depth: Number of wins with that depth
    """
    configurate_plot("Depth", "Number of wins",
                     f"Number of wins after {number_of_games} games with given depth")
    depths = [depth for depth, _ in plot_data.items()]
    wins = [wins for _, wins in plot_data.items()]

    plt_bar = plt.bar(depths, wins, color='#b2e061')
    plt.xticks(ticks=depths)

    bar_counter = 0
    for rect in plt_bar:
        height = rect.get_height()
        plt.annotate(f"{round(height * 100 / number_of_games, 2)}%",
                     (rect.get_x() + rect.get_width() / 2, height + 0.05),
                     ha="center", va="bottom", fontsize=12, label=f"Depth: {depths[bar_counter]}")
        bar_counter += 1

    plt.ylim(0, 1.1 * number_of_games)


def make_data_for_plots(depths: list, number_of_games: int) -> tuple[dict[int, dict], dict[int, int]]:
    data_for_plot_with_scores = dict()
    data_for_plot_with_wins = dict()

    for depth in tqdm(depths, desc="Checked depth counter", unit="depths",
                      colour="#84cc16"):
        single_plot_data = dict()
        single_plot_data["number_of_game"] = range(1, number_of_games + 1)

        scores = []
        wins = 0
        for _ in tqdm(range(number_of_games), desc=f"Games with depth {depth} counter",
                      unit="games", colour="#ecfccb"):
            board = Board(game_start=True)
            game = Game(board)

            run = True
            while run:
                if Game.check_if_blocked(game.board):
                    if Game.check_for_win(game.board):
                        wins += 1
                    scores.append(game.score)
                    run = False
                    continue

                _, best_direction = expectimax(game.board, depth, True)
                if best_direction:
                    game.move_and_check_if_moved(best_direction, if_save_last_move=False)
                    game.board.add_new_random_field()

        single_plot_data["scores"] = scores
        data_for_plot_with_scores[depth] = single_plot_data

        data_for_plot_with_wins[depth] = wins

    return data_for_plot_with_scores, data_for_plot_with_wins


def main():
    num_of_games = 10
    plot_data_scores, plot_data_wins = make_data_for_plots([3, 4], num_of_games)

    make_plot_with_scores(plot_data_scores)
    show_legend()
    save_plot("Plots/plot_scores.png")
    clear_after_making_plot()

    make_plot_with_wins(plot_data_wins, num_of_games)
    save_plot("plots/plot_wins.png")
    clear_after_making_plot()


if __name__ == "__main__":
    main()
