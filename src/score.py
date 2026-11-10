"""Score and UI overlay rendering for Pygame Pong."""

from __future__ import annotations

import pygame

from src.constants import (
    BLACK,
    FONT_SIZE_MESSAGE,
    FONT_SIZE_NAME,
    FONT_SIZE_SCORE,
    FONT_SIZE_SMALL,
    GRAY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TARGET_SCORE,
    WHITE,
)


class Score:
    """Tracks player scores and renders the scoreboard and UI messages."""

    def __init__(
        self,
        screen_width: int = SCREEN_WIDTH,
        screen_height: int = SCREEN_HEIGHT,
        target_score: int = TARGET_SCORE,
        player1_name: str = "Player 1",
        player2_name: str = "Player 2",
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player1_score = 0
        self.player2_score = 0
        self.target_score = target_score
        self.player1_name = player1_name.strip() or "Player 1"
        self.player2_name = player2_name.strip() or "Player 2"
        self.font: pygame.font.Font | None = None
        self.message_font: pygame.font.Font | None = None
        self.name_font: pygame.font.Font | None = None
        self.small_font: pygame.font.Font | None = None

    def _ensure_fonts(self) -> None:
        """Lazily initialize fonts once pygame.font is ready."""
        if self.font is None and pygame.font.get_init():
            try:
                self.font = pygame.font.Font(None, FONT_SIZE_SCORE)
                self.message_font = pygame.font.Font(None, FONT_SIZE_MESSAGE)
                self.name_font = pygame.font.Font(None, FONT_SIZE_NAME)
                self.small_font = pygame.font.Font(None, FONT_SIZE_SMALL)
            except (pygame.error, OSError, RuntimeError):
                self.font = None
                self.message_font = None
                self.name_font = None
                self.small_font = None

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
            return self.player1_name
        elif self.player2_score >= self.target_score:
            return self.player2_name
        return None

    def set_player_name(self, player: int, name: str) -> None:
        """Update display name for player 1 or 2."""
        cleaned = name.strip()
        if player == 1:
            self.player1_name = cleaned or "Player 1"
        elif player == 2:
            self.player2_name = cleaned or "Player 2"
        else:
            raise ValueError(f"Invalid player index: {player}. Must be 1 or 2.")

    def set_player_names(
        self, player1: str | None = None, player2: str | None = None
    ) -> None:
        """Update player display names."""
        if player1 is not None:
            self.player1_name = player1.strip() or "Player 1"
        if player2 is not None:
            self.player2_name = player2.strip() or "Player 2"

    def reset(self) -> None:
        """Reset scores to zero."""
        self.player1_score = 0
        self.player2_score = 0

    def draw_speedometer(
        self,
        surface: pygame.Surface,
        speed: float,
        screen_width: int | None = None,
    ) -> None:
        """Render ball speed indicator on the surface."""
        self._ensure_fonts()
        if self.small_font is None:
            return
        width = screen_width if screen_width is not None else self.screen_width
        center_x = width // 2
        speed_text = f"Speed: {speed:.1f}"
        speed_surf = self.small_font.render(speed_text, True, WHITE, BLACK)
        surface.blit(
            speed_surf,
            (center_x - speed_surf.get_width() // 2, 25),
        )

    def draw(
        self,
        surface: pygame.Surface,
        screen_width: int | None = None,
        screen_height: int | None = None,
        ball_speed: float | None = None,
    ) -> None:
        """Draw the center line and scoreboard on the surface."""
        self._ensure_fonts()

        width = screen_width if screen_width is not None else self.screen_width
        height = screen_height if screen_height is not None else self.screen_height

        # Center dashed net
        dash_length = 15
        gap = 10
        center_x = width // 2
        y = 0
        while y < height:
            pygame.draw.line(
                surface,
                GRAY,
                (center_x, y),
                (center_x, min(y + dash_length, height)),
                2,
            )
            y += dash_length + gap

        # Render score numbers
        if self.font is not None:
            p1_surf = self.font.render(str(self.player1_score), True, WHITE)
            p2_surf = self.font.render(str(self.player2_score), True, WHITE)
            surface.blit(p1_surf, (width // 4 - p1_surf.get_width() // 2, 20))
            surface.blit(p2_surf, (3 * width // 4 - p2_surf.get_width() // 2, 20))

        # Render player names
        if self.name_font is not None:
            p1_name_surf = self.name_font.render(self.player1_name, True, GRAY)
            p2_name_surf = self.name_font.render(self.player2_name, True, GRAY)
            surface.blit(
                p1_name_surf, (width // 4 - p1_name_surf.get_width() // 2, 65)
            )
            surface.blit(
                p2_name_surf, (3 * width // 4 - p2_name_surf.get_width() // 2, 65)
            )

        # Render speedometer during active play
        if ball_speed is not None and not self.is_game_over():
            self.draw_speedometer(surface, ball_speed, width)

        # Game over screen
        if self.is_game_over() and self.message_font is not None:
            winner = self.get_winner()
            msg = f"{winner} Wins!"
            win_surf = self.message_font.render(msg, True, WHITE)
            sub_surf = self.message_font.render(
                "Press SPACE or P to Restart, M for Menu, or ESC to Quit", True, GRAY
            )
            surface.blit(
                win_surf,
                (center_x - win_surf.get_width() // 2, height // 2 - 40),
            )
            surface.blit(
                sub_surf,
                (center_x - sub_surf.get_width() // 2, height // 2 + 10),
            )

    def draw_pause(
        self,
        surface: pygame.Surface,
        screen_width: int | None = None,
        screen_height: int | None = None,
    ) -> None:
        """Render pause message overlay."""
        self._ensure_fonts()
        if self.message_font is not None:
            width = screen_width if screen_width is not None else self.screen_width
            height = screen_height if screen_height is not None else self.screen_height
            center_x = width // 2
            pause_surf = self.message_font.render("PAUSED", True, WHITE)
            hint_surf = self.message_font.render(
                "Press P or SPACE to Resume", True, GRAY
            )
            surface.blit(
                pause_surf,
                (
                    center_x - pause_surf.get_width() // 2,
                    height // 2 - 30,
                ),
            )
            surface.blit(
                hint_surf,
                (
                    center_x - hint_surf.get_width() // 2,
                    height // 2 + 15,
                ),
            )
