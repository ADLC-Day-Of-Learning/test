"""Unit tests for the SoundManager."""

from src.sound import SoundManager


def test_sound_manager_graceful_fallback():
    # SoundManager should initialize cleanly without throwing exceptions
    # even when audio device or mixer is unavailable.
    sound = SoundManager(enabled=True)
    sound.play_bounce()
    sound.play_wall()
    sound.play_score()

    # Disabled sound manager
    sound_disabled = SoundManager(enabled=False)
    sound_disabled.play_bounce()
    sound_disabled.play_wall()
    sound_disabled.play_score()
