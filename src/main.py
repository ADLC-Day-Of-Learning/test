"""Main game entry point and game loop for Pygame Pong."""

import os
import sys

# Ensure project root is on sys.path when executed directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pygame

from src.ball import Ball
from src.constants import (
    BLACK,
    FPS,
    PADDLE_HEIGHT,
    PADDLE_MARGIN,
    PADDLE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WINDOW_TITLE,
)
from src.paddle import Paddle
from src.score import Score
from src.sound import SoundManager


class PongGame:
    """Encapsulates the Pong game state, event handling, physics, and rendering."""

    def __init__(
        self,
        screen_width: int = SCREEN_WIDTH,
        screen_height: int = SCREEN_HEIGHT,
        sound_enabled: bool = True,
        headless: bool = False,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.headless = headless
        self.running = True
        self.paused = False

        if not pygame.get_init():
            pygame.init()

        if not headless:
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height)
            )
            pygame.display.set_caption(WINDOW_TITLE)
        else:
            self.screen = pygame.Surface((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()
        self.sound = SoundManager(enabled=sound_enabled)

        # Initialize paddles (vertically centered)
        p1_x = PADDLE_MARGIN
        p1_y = (self.screen_height - PADDLE_HEIGHT) / 2.0
        self.paddle1 = Paddle(p1_x, p1_y, screen_height=self.screen_height)

        p2_x = self.screen_width - PADDLE_MARGIN - PADDLE_WIDTH
        p2_y = (self.screen_height - PADDLE_HEIGHT) / 2.0
        self.paddle2 = Paddle(p2_x, p2_y, screen_height=self.screen_height)

        # Initialize ball and scoreboard
        self.ball = Ball(
            screen_width=self.screen_width, screen_height=self.screen_height
        )
        self.score = Score()

    def handle_input(self) -> None:
        """Process keyboard events and continuous user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                elif event.key in (pygame.K_p, pygame.K_SPACE):
                    if self.score.is_game_over():
                        self.restart()
                    else:
                        self.paused = not self.paused

        # Handle paddle movement when not paused or game over
        if not self.paused and not self.score.is_game_over():
            keys = pygame.key.get_pressed()
            # Player 1 controls (W/S)
            if keys[pygame.K_w]:
                self.paddle1.move_up()
            if keys[pygame.K_s]:
                self.paddle1.move_down()

            # Player 2 controls (Up/Down)
            if keys[pygame.K_UP]:
                self.paddle2.move_up()
            if keys[pygame.K_DOWN]:
                self.paddle2.move_down()

    def update(self) -> None:
        """Advance game physics, handle collisions, and manage scoring."""
        if self.paused or self.score.is_game_over():
            return

        self.ball.update()

        # Wall collisions (top and bottom)
        if self.ball.check_wall_collision():
            self.sound.play_wall()

        # Paddle collisions
        if self.ball.check_paddle_collision(
            self.paddle1
        ) or self.ball.check_paddle_collision(self.paddle2):
            self.sound.play_bounce()

        # Scoring / out-of-bounds check
        out = self.ball.check_out_of_bounds()
        if out == 1:
            # Player 1 scores point
            self.score.player1_point()
            self.sound.play_score()
            self.ball.reset(direction=-1)
        elif out == -1:
            # Player 2 scores point
            self.score.player2_point()
            self.sound.play_score()
            self.ball.reset(direction=1)

    def draw(self) -> None:
        """Render all game components and UI to the screen."""
        self.screen.fill(BLACK)
        self.score.draw(self.screen, self.screen_width, self.screen_height)
        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        self.ball.draw(self.screen)

        if self.paused:
            self.score.draw_pause(self.screen, self.screen_width, self.screen_height)

        if not self.headless:
            pygame.display.flip()

    def restart(self) -> None:
        """Reset the game state to play again."""
        self.score.reset()
        self.ball.reset()
        self.paddle1.reset()
        self.paddle2.reset()
        self.paused = False

    def step(self) -> None:
        """Execute a single game frame."""
        self.handle_input()
        self.update()
        self.draw()

    def run(self) -> None:
        """Run the main game loop until quit is requested."""
        while self.running:
            self.step()
            self.clock.tick(FPS)


def main() -> None:
    """Launch the Pong game."""
    game = PongGame()
    try:
        game.run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
