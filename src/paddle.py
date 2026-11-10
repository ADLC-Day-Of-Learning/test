"""Paddle module representing player-controlled paddles."""

from __future__ import annotations

import pygame

from src.constants import (
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
)


class Paddle:
    """Represents a movable player paddle bounded within the screen."""

    def __init__(
        self,
        x: float,
        y: float,
        width: int = PADDLE_WIDTH,
        height: int = PADDLE_HEIGHT,
        speed: float = PADDLE_SPEED,
        screen_height: int = SCREEN_HEIGHT,
        color: tuple[int, int, int] = WHITE,
    ):
        self.initial_x = float(x)
        self.initial_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.speed = float(speed)
        self.screen_height = screen_height
        self.color = color

    @property
    def rect(self) -> pygame.Rect:
        """Returns the current pygame.Rect bounding box for the paddle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def move_up(self) -> None:
        """Move paddle upwards, clamped at the top screen boundary (y=0)."""
        self.y = max(0.0, self.y - self.speed)

    def move_down(self) -> None:
        """Move paddle downwards, clamped at the bottom screen boundary."""
        max_y = float(self.screen_height - self.height)
        self.y = min(self.y + self.speed, max_y)

    def reset(self) -> None:
        """Reset paddle to its initial starting position."""
        self.x = self.initial_x
        self.y = self.initial_y

    def draw(self, surface: pygame.Surface) -> None:
        """Render the paddle rectangle onto the target surface."""
        pygame.draw.rect(surface, self.color, self.rect)
