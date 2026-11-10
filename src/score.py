"""Score and UI overlay rendering for Pygame Pong."""

import pygame

from src.constants import (
    FONT_SIZE_MESSAGE,
    FONT_SIZE_SCORE,
    GRAY,
    TARGET_SCORE,
    WHITE,
)


class Score:
    """Tracks player scores and renders the scoreboard and UI messages."""

    def __init__(self, target_score: int = TARGET_SCORE):
        self.player1_score = 0
        self.player2_score = 0
        self.target_score = target_score
        self.font: pygame.font.Font | None = None
        self.message_font: pygame.font.Font | None = None

    def _ensure_fonts(self) -> None:
        """Lazily initialize fonts once pygame.font is ready."""
        if self.font is None and pygame.font.get_init():
            try:
                self.font = pygame.font.Font(None, FONT_SIZE_SCORE)
                self.message_font = pygame.font.Font(None, FONT_SIZE_MESSAGE)
            except (pygame.error, OSError, RuntimeError):
                self.font = None
                self.message_font = None

    def player1_point(self) -> None:
        """Increment score for player 1."""
        self.player1_score += 1

    def player2_point(self) -> None:
        """Increment score for player 2."""
        self.player2_score += 1

    def is_game_over(self) -> bool:
        """Return True if either player has reached the target score."""
        return (
            self.player1_score >= self.target_score
            or self.player2_score >= self.target_score
        )

    def get_winner(self) -> str | None:
        """Return winning player name if game is over, otherwise None."""
        if self.player1_score >= self.target_score:
            return "Player 1"
        elif self.player2_score >= self.target_score:
            return "Player 2"
        return None

    def reset(self) -> None:
        """Reset scores to zero."""
        self.player1_score = 0
        self.player2_score = 0

    def draw(
        self, surface: pygame.Surface, screen_width: int, screen_height: int
    ) -> None:
        """Draw the center line and scoreboard on the surface."""
        self._ensure_fonts()

        # Center dashed net
        dash_length = 15
        gap = 10
        center_x = screen_width // 2
        y = 0
        while y < screen_height:
            pygame.draw.line(
                surface,
                GRAY,
                (center_x, y),
                (center_x, min(y + dash_length, screen_height)),
                2,
            )
            y += dash_length + gap

        # Render score numbers
        if self.font:
            p1_surf = self.font.render(str(self.player1_score), True, WHITE)
            p2_surf = self.font.render(str(self.player2_score), True, WHITE)
            surface.blit(p1_surf, (screen_width // 4 - p1_surf.get_width() // 2, 20))
            surface.blit(
                p2_surf, (3 * screen_width // 4 - p2_surf.get_width() // 2, 20)
            )

        # Game over screen
        if self.is_game_over() and self.message_font:
            winner = self.get_winner()
            msg = f"{winner} Wins!"
            win_surf = self.message_font.render(msg, True, WHITE)
            sub_surf = self.message_font.render(
                "Press SPACE or P to Restart, or ESC to Quit", True, GRAY
            )
            surface.blit(
                win_surf,
                (center_x - win_surf.get_width() // 2, screen_height // 2 - 40),
            )
            surface.blit(
                sub_surf,
                (center_x - sub_surf.get_width() // 2, screen_height // 2 + 10),
            )

    def draw_pause(
        self, surface: pygame.Surface, screen_width: int, screen_height: int
    ) -> None:
        """Render pause message overlay."""
        self._ensure_fonts()
        if self.message_font:
            center_x = screen_width // 2
            pause_surf = self.message_font.render("PAUSED", True, WHITE)
            hint_surf = self.message_font.render(
                "Press P or SPACE to Resume", True, GRAY
            )
            surface.blit(
                pause_surf,
                (
                    center_x - pause_surf.get_width() // 2,
                    screen_height // 2 - 30,
                ),
            )
            surface.blit(
                hint_surf,
                (
                    center_x - hint_surf.get_width() // 2,
                    screen_height // 2 + 15,
                ),
            )
