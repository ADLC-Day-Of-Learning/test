"""Unit tests for the Paddle class."""

import pygame

from src.constants import BLUE, RED
from src.paddle import Paddle


def test_paddle_initialization():
    paddle = Paddle(x=10, y=50, width=15, height=90, speed=5, screen_height=600)
    assert paddle.x == 10.0
    assert paddle.y == 50.0
    assert paddle.width == 15
    assert paddle.height == 90
    assert paddle.speed == 5.0
    assert paddle.rect == pygame.Rect(10, 50, 15, 90)


def test_paddle_movement_bounds():
    """Verify paddle movement stays within screen dimensions.

    Paddle cannot move above y=0 or below y=(screen_height - paddle_height).
    """
    screen_height = 600
    paddle_height = 100
    speed = 20

    paddle = Paddle(
        x=30,
        y=10,
        width=15,
        height=paddle_height,
        speed=speed,
        screen_height=screen_height,
    )

    # Move up past top bound
    paddle.move_up()
    assert paddle.y == 0.0
    paddle.move_up()
    assert paddle.y == 0.0

    # Move down towards bottom bound
    paddle.y = screen_height - paddle_height - 10
    paddle.move_down()
    max_expected_y = float(screen_height - paddle_height)
    assert paddle.y == max_expected_y

    # Move down again, ensure it does not exceed bottom bound
    paddle.move_down()
    assert paddle.y == max_expected_y


def test_paddle_reset():
    paddle = Paddle(x=20, y=150)
    paddle.move_up()
    paddle.move_up()
    assert paddle.y != 150
    paddle.reset()
    assert paddle.x == 20
    assert paddle.y == 150


def test_paddle_draw():
    surface = pygame.Surface((800, 600))
    paddle = Paddle(x=20, y=150)
    paddle.draw(surface)
    # Check that pixels are drawn at the paddle position
    color = surface.get_at((int(paddle.x) + 2, int(paddle.y) + 2))
    assert color[:3] == (255, 255, 255)


def test_paddle_custom_color():
    surface = pygame.Surface((800, 600))
    paddle = Paddle(x=20, y=150, color=RED)
    assert paddle.color == RED
    paddle.draw(surface)
    color = surface.get_at((int(paddle.x) + 2, int(paddle.y) + 2))
    assert color[:3] == RED

    # Change color dynamically
    paddle.color = BLUE
    paddle.draw(surface)
    color = surface.get_at((int(paddle.x) + 2, int(paddle.y) + 2))
    assert color[:3] == BLUE
