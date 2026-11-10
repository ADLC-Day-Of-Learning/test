"""Unit tests for the Ball class."""

import math

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

    # At top boundary but moving downwards - no collision
    ball.y = 0.0
    ball.speed_y = 5.0
    assert ball.check_wall_collision() is False
    assert ball.speed_y == 5.0

    # At bottom boundary but moving upwards - no collision
    ball.y = 600.0 - 15.0
    ball.speed_y = -5.0
    assert ball.check_wall_collision() is False
    assert ball.speed_y == -5.0


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

    # Ball already behind left paddle should not collide
    ball.x = 10
    ball.y = 280
    ball.speed_x = -5.0
    behind_paddle = Paddle(x=15, y=250, width=15, height=100)
    assert ball.check_paddle_collision(behind_paddle) is False

    # Ball already behind right paddle should not collide
    ball.x = 760
    ball.y = 280
    ball.speed_x = 5.0
    behind_right_paddle = Paddle(x=750, y=250, width=15, height=100)
    assert ball.check_paddle_collision(behind_right_paddle) is False


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


def test_ball_current_speed_calculation_and_acceleration():
    """Verify that Ball provides current speed and updates on velocity change."""
    ball = Ball(
        initial_speed_x=BALL_INITIAL_SPEED_X,
        initial_speed_y=BALL_INITIAL_SPEED_Y,
    )
    expected_initial = math.hypot(BALL_INITIAL_SPEED_X, BALL_INITIAL_SPEED_Y)

    # Ball exposes scalar speed
    assert hasattr(ball, "current_speed")
    assert not hasattr(ball, "speed")
    assert math.isclose(ball.current_speed, expected_initial, rel_tol=1e-2)

    # Accelerate velocity and verify current_speed reflects the increase
    ball.speed_x *= ball.speed_increment
    assert ball.current_speed > expected_initial


def test_ball_current_speed_paddle_collision_and_reset():
    """Verify that paddle collision accelerates ball horizontal speed and reset restores it."""
    ball = Ball(
        screen_width=800,
        screen_height=600,
        size=15,
        initial_speed_x=5.0,
        initial_speed_y=5.0,
        speed_increment=1.2,
    )
    expected_initial = math.hypot(5.0, 5.0)
    assert math.isclose(ball.current_speed, expected_initial, rel_tol=1e-5)

    paddle = Paddle(x=30, y=250, width=15, height=100)
    # Position ball near edge of paddle so both speed_x and speed_y result in higher current_speed
    ball.x = 35
    ball.y = 340  # near the bottom of paddle (y=250..350)
    ball.speed_x = -5.0

    collided = ball.check_paddle_collision(paddle)
    assert collided is True
    assert abs(ball.speed_x) > 5.0
    assert ball.current_speed > expected_initial

    # Resetting the ball restores the initial scalar speed
    ball.reset()
    assert math.isclose(ball.current_speed, expected_initial, rel_tol=1e-5)
