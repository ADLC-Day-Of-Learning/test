"""Unit tests for the PongGame loop and mechanics."""

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

    # Move ball past right boundary
    game.ball.x = game.screen_width + 10
    game.update()

    # Player 1 should have scored
    assert game.score.player1_score == 1
    # Ball should have reset to center
    assert game.ball.x == (game.screen_width - game.ball.size) / 2.0


def test_game_restart():
    game = PongGame(headless=True, sound_enabled=False)
    game.score.player1_score = 11
    game.paused = True
    game.restart()

    assert game.score.player1_score == 0
    assert game.score.player2_score == 0
    assert game.paused is False
