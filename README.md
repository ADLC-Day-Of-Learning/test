# Pygame Pong

A classic 2D Pong game implementation built in Python using the [Pygame](https://www.pygame.org/) library.

## Overview

Pong is one of the earliest arcade video games. In this game, two players control paddles on opposite sides of the screen to hit a ball back and forth. A player scores a point whenever the opponent fails to return the ball. The objective is to reach the target score before the opposing player.

## Features

- **Classic Gameplay**: Authentic paddle movement, ball bouncing physics, and score tracking.
- **Controls**: Smooth two-player keyboard controls (W/S and Up/Down arrows).
- **Dynamic Ball Speed**: Ball speed increases with successive paddle hits for added challenge.
- **Audio & Visuals**: Retro sound effects and visual boundary indicators.

## Prerequisites

- **Python 3.8+**
- **Pygame 2.0+**

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ADLC-Day-Of-Learning/test.git
   cd test
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Running the Game

Once dependencies are installed, start the game:

```bash
python src/main.py
```

### Running Tests

To execute the test suite:

```bash
pytest
```

### Controls

| Player | Move Up | Move Down |
| :--- | :--- | :--- |
| **Player 1 (Left)** | `W` | `S` |
| **Player 2 (Right)** | `Up Arrow` (`↑`) | `Down Arrow` (`↓`) |

- **Pause Game:** `P` or `Space`
- **Quit Game:** `ESC` or close window

## Project Structure

```text
.
├── README.md        # Project documentation
├── requirements.txt # Project dependencies
├── src/
│   ├── __init__.py  # Package initialization
│   ├── main.py      # Game entry point and main game loop
│   ├── ball.py      # Ball movement and collision logic
│   ├── paddle.py    # Paddle movement and player input
│   ├── score.py     # Scoreboard and UI rendering
│   ├── sound.py     # Audio manager and sound effects
│   └── constants.py # Game constants (screen dimensions, speeds, colors)
├── tests/           # Unit and integration test suite
│   ├── conftest.py  # Pytest configuration and fixtures
│   ├── test_ball.py # Ball physics and collision tests
│   ├── test_game.py # Game loop and input handling tests
│   ├── test_paddle.py # Paddle movement and bounds tests
│   ├── test_score.py  # Score tracking and UI rendering tests
│   └── test_sound.py  # Sound manager fallback tests
└── assets/
    └── sounds/      # Sound effects for ball bounce and scoring
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
