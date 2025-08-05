# Memory Game - Countries Theme

A Python-based memory card matching game using country data from flagsapi.com.

## Features

- **Grid Options**: Choose from 4x4, 6x6, or 8x8 grids
- **Multiplayer**: Support for 1 or 2 players
- **Country Theme**: Uses country names and flags from flagsapi.com
- **Console Interface**: Clean, easy-to-use console interface
- **API Integration**: Fetches flag data from flagsapi.com (falls back to country names if API unavailable)

## How to Play

1. **Setup**: Choose your grid size and number of players
2. **Objective**: Match pairs of countries by remembering their positions
3. **Turns**: 
   - Enter coordinates (row, column) to flip cards
   - Find matching pairs to score points
   - In 2-player mode, turns alternate unless you find a match
4. **Winning**: Match all pairs to win the game!

## Installation & Running

### Prerequisites
```bash
pip install requests
```

### Running the Game
```bash
python console_memory_game.py
```

## Game Controls

- Enter coordinates as `row column` (e.g., `2 3`)
- Type `quit` to exit the game
- Use Ctrl+C to cancel at any time

## Game Board Example

```
Grid Size: 4x4
Pairs Found: 2

      1   2   3   4
 1    ?   ?  USA   ?
 2   FRA  ?   ?   USA
 3    ?  FRA  ?   ?
 4    ?   ?   ?   ?
```

## API Integration

The game integrates with flagsapi.com to:
- Test API connectivity at startup
- Use country codes for matching logic
- Display country names (3-letter abbreviations)
- Could be extended to show actual flag images in GUI version

## Files

- `console_memory_game.py` - Main console-based game
- `memory_game.py` - GUI version (requires tkinter and Pillow)
- `README.md` - This documentation

## Technical Implementation

- **Language**: Python 3.12+
- **HTTP Requests**: Uses `requests` library for API calls
- **Game Logic**: Implements classic memory game mechanics
- **Data Structure**: 2D arrays for board state management
- **Error Handling**: Graceful fallbacks for network issues

## Country Data

The game includes 32 predefined countries with their ISO codes:
- United States (US), Canada (CA), United Kingdom (GB)
- European countries: France, Germany, Italy, Spain, etc.
- Asian countries: Japan, China, India, South Korea, etc.
- Other regions: Brazil, Australia, South Africa, etc.

## Future Enhancements

- GUI version with actual flag images
- Difficulty levels with timing challenges
- Statistics tracking
- Custom country selections
- Online multiplayer support

---

*This game was developed as part of the GitHub Copilot Hackathon challenge to create a memory game using Python and country data from flagsapi.com.*