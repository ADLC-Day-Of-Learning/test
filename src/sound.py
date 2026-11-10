"""Audio manager for Pong sound effects with graceful fallbacks."""

from __future__ import annotations

import os
import warnings

import pygame

from src.constants import SOUND_BOUNCE, SOUND_SCORE, SOUND_WALL


class SoundManager:
    """Manages audio loading and playback with graceful headless/error fallback."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._bounce_sound: pygame.mixer.Sound | None = None
        self._wall_sound: pygame.mixer.Sound | None = None
        self._score_sound: pygame.mixer.Sound | None = None
        self._initialized = False

        if self.enabled:
            self._init_mixer()

    def _init_mixer(self) -> None:
        """Safely attempt to initialize the pygame mixer and load sound assets."""
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                if not hasattr(pygame, "mixer") or pygame.mixer is None:
                    return
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
            self._initialized = True
            self._load_sounds()
        except (pygame.error, OSError, RuntimeError, ImportError):
            self._initialized = False

    def _load_sounds(self) -> None:
        """Load audio files if available on disk and mixer is active."""
        if not self._initialized:
            return
        try:
            if os.path.exists(SOUND_BOUNCE):
                self._bounce_sound = pygame.mixer.Sound(SOUND_BOUNCE)
            if os.path.exists(SOUND_WALL):
                self._wall_sound = pygame.mixer.Sound(SOUND_WALL)
            if os.path.exists(SOUND_SCORE):
                self._score_sound = pygame.mixer.Sound(SOUND_SCORE)
        except (pygame.error, OSError, RuntimeError):
            pass

    def play_bounce(self) -> None:
        """Play paddle contact sound."""
        if self._bounce_sound and self._initialized:
            try:
                self._bounce_sound.play()
            except (pygame.error, RuntimeError):
                pass

    def play_wall(self) -> None:
        """Play wall reflection sound."""
        if self._wall_sound and self._initialized:
            try:
                self._wall_sound.play()
            except (pygame.error, RuntimeError):
                pass

    def play_score(self) -> None:
        """Play scoring sound."""
        if self._score_sound and self._initialized:
            try:
                self._score_sound.play()
            except (pygame.error, RuntimeError):
                pass
