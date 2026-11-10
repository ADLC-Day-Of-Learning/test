"""Unit tests for Score tracking and UI rendering."""

import pygame

from src.ball import Ball
from src.constants import TARGET_SCORE
from src.score import Score


def test_scoring_and_reset():
    """Verify score increments when ball crosses left or right boundary.

    Verify ball resets to center with initial velocity.
    """
    score = Score(target_score=5)
    ball = Ball(screen_width=800, screen_height=600, size=15)

    # Ball crosses right boundary -> player 1 scores
    ball.x = 810
    out = ball.check_out_of_bounds()
    assert out == 1
    score.player1_point()
    assert score.player1_score == 1
    assert score.player2_score == 0

    ball.reset(direction=-1)
    assert ball.x == (800 - 15) / 2.0
    assert ball.y == (600 - 15) / 2.0
    assert ball.speed_x == -ball.initial_speed_x

    # Ball crosses left boundary -> player 2 scores
    ball.x = -20
    out = ball.check_out_of_bounds()
    assert out == -1
    score.player2_point()
    assert score.player1_score == 1
    assert score.player2_score == 1

    ball.reset(direction=1)
    assert ball.x == (800 - 15) / 2.0
    assert ball.speed_x == ball.initial_speed_x

    # Reset scores
    score.reset()
    assert score.player1_score == 0
    assert score.player2_score == 0


def test_game_over_and_winner():
    score = Score(target_score=3)
    assert score.is_game_over() is False
    assert score.get_winner() is None

    score.player1_point()
    score.player1_point()
    assert score.is_game_over() is False

    score.player1_point()
    assert score.is_game_over() is True
    assert score.get_winner() == "Player 1"

    score.reset()
    assert score.is_game_over() is False

    score.player2_point()
    score.player2_point()
    score.player2_point()
    assert score.is_game_over() is True
    assert score.get_winner() == "Player 2"


def test_score_draw_and_pause_draw():
    surface = pygame.Surface((800, 600))
    score = Score()
    # Draw regular score board
    score.draw(surface, 800, 600)

    # Draw paused overlay
    score.draw_pause(surface, 800, 600)

    # Trigger game over and draw
    score.player1_score = TARGET_SCORE
    score.draw(surface, 800, 600)
