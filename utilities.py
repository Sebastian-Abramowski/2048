import pygame
import csv
import numpy as np
from pathlib import Path
from typing import Union


def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font,
              text_color: tuple[int, int, int], x: int, y: int) -> tuple[int, int]:
    img = font.render(text, True, text_color)
    surface.blit(img, (x, y))

    return img.get_width(), img.get_height()


def get_size_of_text(text: str, font: pygame.font.Font) -> tuple[int, int]:
    img = font.render(text, True, (0, 0, 0))

    return img.get_width(), img.get_height()


def scale_img(image: pygame.Surface, scale: Union[float, int]):
    width = image.get_width()
    height = image.get_height()
    new_iamge = pygame.transform.scale(image, (width * scale, height * scale))
    return new_iamge


def read_best_score_from_file(file_path: Union[Path, str]) -> int:
    with open(file_path, 'r') as file_handle:
        csvreader = csv.reader(file_handle)

        scores = []
        for row in csvreader:
            score = int(row[1])
            scores.append(score)
        return max(scores)


def read_best_player_or_ai_score_from_file(file_path: Union[Path, str], player_or_ai: str) -> int:
    with open(file_path, 'r') as file_handle:
        csvreader = csv.reader(file_handle)
        data = list(csvreader)
        if player_or_ai == "player":
            return int(data[0][1])
        elif player_or_ai == "ai":
            return int(data[1][1])


def update_best_score_in_file(file_path: Union[Path, str], new_best_score: int, if_ai: bool) -> None:
    existing_data = []
    with open(file_path, 'r') as file_handle:
        csvreader = csv.reader(file_handle)
        existing_data = list(csvreader)

    if if_ai:
        existing_data[1][1] = new_best_score
    else:
        existing_data[0][1] = new_best_score

    with open(file_path, 'w', newline='\n') as file_handle:
        csvwriter = csv.writer(file_handle)
        csvwriter.writerows(existing_data)


def remove_none_values_from_the_end_of_numpy_list(values: np.array) -> np.array:
    # it returns copied array, not original
    while np.size(values) > 0 and values[-1] is None:
        values = np.delete(values, -1)
    return values
