"""Unit tests for the PongGame loop and mechanics."""

from collections import defaultdict

import pygame

from src.main import PongGame


def test_game_initialization_headless():
    game = PongGame(headless=True, sound_enabled=False)
    assert game.running is True
    assert game.paused is False
    assert game.paddle1 is not None
    assert game.paddle2 is not None
    assert game.ball is not None
    assert game.score is not None


def test_game_step_and_pause():
    game = PongGame(headless=True, sound_enabled=False)

    # Initial step
    initial_ball_x = game.ball.x
    game.step()
    # Ball should have moved
    assert game.ball.x != initial_ball_x

    # Pause the game
    game.paused = True
    paused_ball_x = game.ball.x
    game.step()
    # Ball should not have moved while paused
    assert game.ball.x == paused_ball_x

    # Unpause
    game.paused = False
    game.step()
    assert game.ball.x != paused_ball_x


def test_game_scoring_updates():
    game = PongGame(headless=True, sound_enabled=False)

    # Move ball past right boundary -> Player 1 scores
    game.ball.x = game.screen_width + 10
    game.update()

    # Player 1 should have scored
    assert game.score.player1_score == 1
    # Ball should have reset to center
    assert game.ball.x == (game.screen_width - game.ball.size) / 2.0

    # Move ball past left boundary -> Player 2 scores
    game.ball.x = -20
    game.update()

    # Player 2 should have scored
    assert game.score.player2_score == 1
    # Ball should have reset to center with rightward direction
    assert game.ball.x == (game.screen_width - game.ball.size) / 2.0
    assert game.ball.speed_x > 0


def test_game_restart():
    game = PongGame(headless=True, sound_enabled=False)
    game.score.player1_score = 11
    game.paused = True
    game.restart()

    assert game.score.player1_score == 0
    assert game.score.player2_score == 0
    assert game.paused is False


def test_game_handle_input_quit_events():
    """Verify handle_input handles QUIT and ESCAPE events."""
    game = PongGame(headless=True, sound_enabled=False)

    # QUIT event
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.handle_input()
    assert game.running is False

    # ESCAPE key event
    game.running = True
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    game.handle_input()
    assert game.running is False


def test_game_handle_input_pause_and_restart():
    """Verify handle_input toggles pause and restarts game over."""
    game = PongGame(headless=True, sound_enabled=False)

    # Toggle pause with 'P'
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
    game.handle_input()
    assert game.paused is True

    # Toggle pause with SPACE
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game.handle_input()
    assert game.paused is False

    # Restart game on SPACE when game over
    game.score.player1_score = 11
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    game.handle_input()
    assert game.score.player1_score == 0
    assert game.paused is False


def test_game_handle_input_paddle_movement(monkeypatch):
    """Verify handle_input moves paddles based on key state."""
    game = PongGame(headless=True, sound_enabled=False)

    initial_p1_y = game.paddle1.y
    initial_p2_y = game.paddle2.y

    # Move Player 1 up (W) and Player 2 down (DOWN)
    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: defaultdict(bool, {pygame.K_w: True, pygame.K_DOWN: True}),
    )
    game.handle_input()
    assert game.paddle1.y < initial_p1_y
    assert game.paddle2.y > initial_p2_y

    # Move Player 1 down (S) and Player 2 up (UP)
    p1_current_y = game.paddle1.y
    p2_current_y = game.paddle2.y
    monkeypatch.setattr(
        pygame.key,
        "get_pressed",
        lambda: defaultdict(bool, {pygame.K_s: True, pygame.K_UP: True}),
    )
    game.handle_input()
    assert game.paddle1.y > p1_current_y
    assert game.paddle2.y < p2_current_y


def test_game_step_stops_when_not_running():
    """Verify step immediately returns without updating or drawing if running is False."""
    game = PongGame(headless=True, sound_enabled=False)
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    initial_ball_x = game.ball.x
    game.step()
    assert game.running is False
    # Ball should not have moved because step returned early
    assert game.ball.x == initial_ball_x
