# Memory Game - Colors Edition 🎨

A Python implementation of the classic memory matching game using colors as card symbols.

## Overview

This Memory Game challenges players to match pairs of colored cards in a grid. Players take turns flipping two cards at a time, trying to find matching color pairs. The goal is to match all pairs with the fewest attempts.

## Features

### ✨ Game Features
- **Color-based cards**: 8+ different colors with visual representation
- **Multiple grid sizes**: 4×4 (16 cards) and 6×6 (36 cards) options
- **1-2 player support**: Single player or competitive two-player mode
- **Console interface**: Text-based UI that works in any terminal
- **Score tracking**: Points system for competitive play
- **Visual feedback**: Color-coded display with ANSI colors

### 🎮 Game Mechanics
- Cards start face down in a randomized grid
- Players select two cards per turn by entering coordinates
- Matching pairs remain face up and score points
- Non-matching cards flip back face down after a brief display
- Game ends when all pairs are matched
- Winner determined by most pairs found (2-player mode)

## Requirements

- Python 3.6 or higher
- Terminal with ANSI color support (most modern terminals)

## Installation & Running

### Option 1: Console Version (Recommended)
```bash
# Navigate to the memory game directory
cd challenges/memorygame

# Run the console version
python3 memory_game_console.py
```

### Option 2: GUI Version (if tkinter is available)
```bash
# Run the GUI version
python3 memory_game.py
```

## How to Play

### Game Setup
1. Choose number of players (1 or 2)
2. Select grid size:
   - **4×4**: 16 cards, 8 pairs (easier)
   - **6×6**: 36 cards, 18 pairs (challenging)

### Gameplay
1. **Single Player**: Match all pairs to win
2. **Two Player**: Take turns; player with most pairs wins

### Controls
- Enter card positions as `row,col` (e.g., `2,3`) or `rc` format (e.g., `23`)
- Grid positions are numbered 1-4 (or 1-6) for both rows and columns

### Example Turn
```
Current Board:
=========================
    1    2    3    4  
1 |  ? |  ? |  ? |  ? |
2 |  ? |  ? |  ? |  ? |
3 |  ? |  ? |  ? |  ? |
4 |  ? |  ? |  ? |  ? |
=========================

Select first card: 1,1
Revealed: Red at position (1,1)

Select second card: 2,3  
Revealed: Blue at position (2,3)
❌ No match. Cards will be hidden again.
```

## Color Legend

The game uses the following colors:
- **R** - Red
- **G** - Green  
- **B** - Blue
- **Y** - Yellow
- **M** - Magenta
- **C** - Cyan
- **O** - Orange
- **P** - Purple
- Plus additional colors for 6×6 mode

## Testing

Run the automated test suite to verify game functionality:

```bash
python3 test_memory_game.py
```

The tests verify:
- ✅ Game initialization
- ✅ Deck creation and shuffling
- ✅ Card matching logic
- ✅ Win condition detection
- ✅ Two-player mode
- ✅ Different grid sizes

## Implementation Details

### Architecture
- **Object-oriented design** with clean separation of concerns
- **Game state management** for tracking cards, players, and scores
- **Modular functions** for easy testing and maintenance

### Key Components
- `MemoryGame` class: Main game controller
- Card grid system with 2D arrays
- Player management and turn switching
- Color-coded terminal display
- Input validation and error handling

### File Structure
```
memorygame/
├── memory_game_console.py    # Console version (main implementation)
├── memory_game.py           # GUI version (tkinter)
├── test_memory_game.py      # Automated test suite
├── README.md               # This documentation
└── memorygame.md          # Original challenge description
```

## Challenge Requirements ✅

This implementation fulfills all requirements from `memorygame.md`:

1. **✅ Programming language**: Python (as specified)
2. **✅ Card topic**: Colors (as specified) 
3. **✅ Grid system**: 4×4 and 6×6 grids implemented
4. **✅ Player support**: 1-2 players supported
5. **✅ Card mechanics**: Click/select to flip cards
6. **✅ Shuffle**: Cards randomly distributed
7. **✅ Match detection**: Pair matching logic implemented
8. **✅ Win condition**: Game ends when all pairs matched

## Development Notes

This game was developed following the CopilotHackathon challenge guidelines:
- Used Python as the specified programming language
- Implemented colors as the card topic as requested
- Followed all development steps from the challenge instructions
- Added comprehensive testing to ensure reliability
- Created both console and GUI versions for maximum compatibility

## Contributing

Feel free to enhance the game with additional features:
- More color options
- Different themes (animals, shapes, etc.)
- Sound effects
- High score tracking
- Network multiplayer
- Mobile-friendly version

---

**Enjoy the Memory Game! 🧠🎮**