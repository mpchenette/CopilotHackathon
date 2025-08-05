# Memory Game

A console-based memory game implementation in Python using colors as card symbols.

## Overview

This is a classic memory matching game where players flip cards to find matching pairs. The game uses color names as the symbols on the cards.

## Features

- **Multiple Grid Sizes**: Choose from 4x4, 6x6, or 8x8 grids
- **Single or Two-Player Mode**: Play alone or compete with a friend
- **Color-Based Cards**: Uses various color names as card symbols
- **Score Tracking**: Keeps track of matches found by each player
- **Console Interface**: Easy-to-use text-based interface

## Requirements

- Python 3.6 or higher
- No external dependencies required

## How to Play

1. Run the game:
   ```bash
   python memory_game.py
   ```

2. Choose your grid size (4, 6, or 8)
3. Choose number of players (1 or 2)
4. The game will display a grid with hidden cards marked as "?"
5. Enter row and column numbers to flip cards (e.g., "2 3")
6. Try to find matching color pairs
7. The game ends when all pairs are matched

## Game Rules

- Each turn, flip exactly two cards
- If the cards match, they stay revealed and you score a point
- If they don't match, they flip back over after a brief display
- In two-player mode, players alternate turns unless they find a match
- The player with the most matches wins (two-player mode)

## Files

- `memory_game.py` - Main game implementation
- `test_memory_game.py` - Unit tests for the game logic
- `demo.py` - Demonstration script showing game functionality

## Testing

Run the unit tests to verify the game functionality:

```bash
python test_memory_game.py
```

Run the demo to see a quick demonstration:

```bash
python demo.py
```

## Implementation Details

The game implements all the requirements from the challenge:

- ✅ **Python Programming Language**: Written in Python
- ✅ **Colors Topic**: Uses color names as card symbols
- ✅ **Grid Creation**: Supports 4x4, 6x6, and 8x8 grids
- ✅ **Player Selection**: Supports 1 or 2 players
- ✅ **Card Management**: Cards have symbols (colors) and can be flipped
- ✅ **Shuffling**: Cards are randomly shuffled at game start
- ✅ **Click Events**: Console input simulates card clicking
- ✅ **Match Detection**: Properly detects and handles matching pairs
- ✅ **Win Condition**: Game ends when all pairs are matched

## Example Gameplay

```
Memory Game Setup
================
Choose grid size (4, 6, or 8): 4
Choose number of players (1 or 2): 1

Welcome to the Memory Game!
Match pairs of colors by remembering their positions.
Enter row and column numbers to flip cards (e.g., '2 3').
Type 'quit' to exit the game.

==================================================
MEMORY GAME - Player 1's Turn
Matches found: 0
==================================================

     1  2  3  4
 1  ?  ?  ?  ? 
 2  ?  ?  ?  ? 
 3  ?  ?  ?  ? 
 4  ?  ?  ?  ? 

Player 1, enter row and column (e.g., '2 3') or 'quit': 1 1
```

## Available Colors

The game includes 32 different colors to support even the largest 8x8 grid:
- RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE
- PINK, BROWN, BLACK, WHITE, GRAY, CYAN
- MAGENTA, LIME, NAVY, MAROON, OLIVE, TEAL
- GOLD, SILVER, CORAL, SALMON, INDIGO, VIOLET
- TAN, BEIGE, KHAKI, AZURE, IVORY, CRIMSON
- SCARLET, RUBY