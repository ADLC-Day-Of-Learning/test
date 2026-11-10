"""Unit tests for the Ball class."""

from src.ball import Ball
from src.constants import (
    BALL_INITIAL_SPEED_X,
    BALL_INITIAL_SPEED_Y,
)
from src.paddle import Paddle


def test_ball_initialization():
    ball = Ball(screen_width=800, screen_height=600, size=15)
    assert ball.screen_width == 800
    assert ball.screen_height == 600
    assert ball.size == 15
    assert ball.x == (800 - 15) / 2.0
    assert ball.y == (600 - 15) / 2.0
    assert ball.speed_x == BALL_INITIAL_SPEED_X
    assert ball.speed_y == BALL_INITIAL_SPEED_Y


def test_ball_movement():
    ball = Ball()
    start_x = ball.x
    start_y = ball.y
    ball.update()
    assert ball.x == start_x + ball.speed_x
    assert ball.y == start_y + ball.speed_y


def test_ball_wall_collision():
    ball = Ball(screen_height=600, size=15)

    # Top wall collision
    ball.y = -2.0
    ball.speed_y = -5.0
    assert ball.check_wall_collision() is True
    assert ball.y == 0.0
    assert ball.speed_y == 5.0  # Inverted

    # Bottom wall collision
    ball.y = 600.0
    ball.speed_y = 5.0
    assert ball.check_wall_collision() is True
    assert ball.y == 600.0 - 15.0
    assert ball.speed_y == -5.0  # Inverted

    # Middle of screen - no collision
    ball.y = 300.0
    ball.speed_y = 5.0
    assert ball.check_wall_collision() is False
    assert ball.speed_y == 5.0


def test_ball_paddle_collision_and_speedup():
    """Verify ball horizontal direction inverts on paddle contact.

    Verify ball speed increases by multiplier after paddle hit.
    """
    ball = Ball(
        screen_width=800,
        screen_height=600,
        size=15,
        initial_speed_x=5.0,
        speed_increment=1.1,
    )
    left_paddle = Paddle(x=30, y=250, width=15, height=100)

    # Position ball moving left, intersecting left paddle
    ball.x = 35
    ball.y = 280
    ball.speed_x = -5.0

    collided = ball.check_paddle_collision(left_paddle)
    assert collided is True
    # Verify horizontal direction inverted (now moving right)
    assert ball.speed_x > 0
    # Verify speed increased by multiplier
    expected_speed_x = 5.0 * 1.1
    assert abs(ball.speed_x - expected_speed_x) < 1e-5
    # Verify repositioned outside paddle
    assert ball.x == float(left_paddle.rect.right)

    # Now test right paddle collision
    right_paddle = Paddle(x=750, y=250, width=15, height=100)
    ball.x = 745
    ball.y = 280
    ball.speed_x = 6.0

    collided = ball.check_paddle_collision(right_paddle)
    assert collided is True
    # Verify horizontal direction inverted (now moving left)
    assert ball.speed_x < 0
    expected_speed_x_2 = 6.0 * 1.1
    assert abs(abs(ball.speed_x) - expected_speed_x_2) < 1e-5
    assert ball.x == float(right_paddle.rect.left - ball.size)


def test_ball_max_speed_cap():
    ball = Ball(
        initial_speed_x=14.0,
        speed_increment=1.5,
        max_speed=15.0,
    )
    paddle = Paddle(x=30, y=250, width=15, height=100)
    ball.x = 35
    ball.y = 280
    ball.speed_x = -14.0

    ball.check_paddle_collision(paddle)
    assert ball.speed_x == 15.0  # Capped at max_speed


def test_ball_out_of_bounds():
    ball = Ball(screen_width=800, size=15)

    # In play
    ball.x = 400
    assert ball.check_out_of_bounds() == 0

    # Past left boundary
    ball.x = -20
    assert ball.check_out_of_bounds() == -1

    # Past right boundary
    ball.x = 805
    assert ball.check_out_of_bounds() == 1


def test_ball_reset():
    ball = Ball(
        screen_width=800,
        screen_height=600,
        size=15,
        initial_speed_x=5.0,
        initial_speed_y=5.0,
    )
    ball.x = 10
    ball.y = 20
    ball.speed_x = 12.0
    ball.speed_y = 12.0

    ball.reset(direction=1)
    assert ball.x == (800 - 15) / 2.0
    assert ball.y == (600 - 15) / 2.0
    assert ball.speed_x == 5.0
    assert ball.speed_y == 5.0

    ball.reset(direction=-1)
    assert ball.speed_x == -5.0
