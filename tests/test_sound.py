"""Unit tests for the SoundManager."""

from src.sound import SoundManager


def test_sound_manager_graceful_fallback():
    """Verify SoundManager initializes cleanly without throwing exceptions.

    Ensure graceful fallback when audio device or mixer is unavailable.
    """
    sound = SoundManager(enabled=True)
    assert sound.enabled is True
    sound.play_bounce()
    sound.play_wall()
    sound.play_score()

    # Disabled sound manager
    sound_disabled = SoundManager(enabled=False)
    assert sound_disabled.enabled is False
    assert sound_disabled._initialized is False
    sound_disabled.play_bounce()
    sound_disabled.play_wall()
    sound_disabled.play_score()
