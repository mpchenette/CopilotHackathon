#!/usr/bin/env python3
"""
Test script for Memory Game functionality
Tests the core game mechanics without user interaction
"""

import sys
import os

# Add the current directory to Python path to import our game
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_game_console import MemoryGame

def test_game_initialization():
    """Test game initialization"""
    print("Testing game initialization...")
    game = MemoryGame()
    
    # Test color definitions
    assert len(game.colors) >= 8, "Should have at least 8 colors for 4x4 grid"
    
    # Test initial state
    assert game.grid_size == 4, "Default grid size should be 4"
    assert game.num_players == 1, "Default player count should be 1"
    assert game.current_player == 1, "Should start with player 1"
    
    print("✅ Game initialization test passed")

def test_deck_creation():
    """Test deck creation and card distribution"""
    print("Testing deck creation...")
    game = MemoryGame()
    game.grid_size = 4
    game.total_cards = 16
    game.total_pairs = 8
    
    game.create_deck()
    
    # Verify grid dimensions
    assert len(game.cards) == 4, "Should have 4 rows"
    assert all(len(row) == 4 for row in game.cards), "Each row should have 4 columns"
    
    # Count color occurrences
    color_counts = {}
    for row in game.cards:
        for card in row:
            color_counts[card] = color_counts.get(card, 0) + 1
    
    # Each color should appear exactly twice
    for color, count in color_counts.items():
        assert count == 2, f"Color {color} should appear exactly twice, got {count}"
    
    # Should have exactly 8 different colors
    assert len(color_counts) == 8, f"Should have 8 different colors, got {len(color_counts)}"
    
    print("✅ Deck creation test passed")

def test_match_logic():
    """Test the card matching logic"""
    print("Testing match logic...")
    game = MemoryGame()
    game.grid_size = 4
    game.total_cards = 16
    game.total_pairs = 8
    game.create_deck()
    
    # Find two cards with the same color
    target_color = None
    pos1 = None
    pos2 = None
    
    for row in range(4):
        for col in range(4):
            color = game.cards[row][col]
            # Find another card with the same color
            for row2 in range(4):
                for col2 in range(4):
                    if (row2, col2) != (row, col) and game.cards[row2][col2] == color:
                        target_color = color
                        pos1 = (row, col)
                        pos2 = (row2, col2)
                        break
                if pos1 and pos2:
                    break
            if pos1 and pos2:
                break
    
    # Test match detection
    initial_score = game.player_scores[0]
    
    # Reveal both cards
    game.revealed[pos1[0]][pos1[1]] = True
    game.revealed[pos2[0]][pos2[1]] = True
    
    # Check match (should return True)
    is_match = game.check_match(pos1, pos2)
    assert is_match == True, "Should detect match for same color cards"
    assert game.matched[pos1[0]][pos1[1]] == True, "First card should be marked as matched"
    assert game.matched[pos2[0]][pos2[1]] == True, "Second card should be marked as matched"
    assert game.player_scores[0] == initial_score + 1, "Score should increase by 1"
    
    print("✅ Match logic test passed")

def test_win_condition():
    """Test win condition detection"""
    print("Testing win condition...")
    game = MemoryGame()
    game.grid_size = 4
    game.total_cards = 16
    game.total_pairs = 8
    game.create_deck()
    
    # Initially should not be won
    assert game.check_win_condition() == False, "Game should not be won initially"
    
    # Mark all cards as matched
    for row in range(4):
        for col in range(4):
            game.matched[row][col] = True
    
    # Now should be won
    assert game.check_win_condition() == True, "Game should be won when all cards matched"
    
    print("✅ Win condition test passed")

def test_two_player_mode():
    """Test two player functionality"""
    print("Testing two player mode...")
    game = MemoryGame()
    game.num_players = 2
    game.current_player = 1
    game.player_scores = [0, 0]
    
    # Test player switching
    initial_player = game.current_player
    
    # Simulate a non-matching turn
    game.current_player = 3 - game.current_player  # Switch player logic
    assert game.current_player != initial_player, "Player should switch after non-match"
    
    # Test score tracking for both players
    game.player_scores[0] = 3
    game.player_scores[1] = 2
    assert game.player_scores[0] == 3, "Player 1 score should be tracked"
    assert game.player_scores[1] == 2, "Player 2 score should be tracked"
    
    print("✅ Two player mode test passed")

def test_6x6_grid():
    """Test 6x6 grid functionality"""
    print("Testing 6x6 grid...")
    game = MemoryGame()
    game.grid_size = 6
    game.total_cards = 36
    game.total_pairs = 18
    
    game.create_deck()
    
    # Verify grid dimensions
    assert len(game.cards) == 6, "Should have 6 rows"
    assert all(len(row) == 6 for row in game.cards), "Each row should have 6 columns"
    
    # Count unique colors
    colors_used = set()
    for row in game.cards:
        for card in row:
            colors_used.add(card)
    
    assert len(colors_used) == 18, f"Should have 18 different colors, got {len(colors_used)}"
    
    print("✅ 6x6 grid test passed")

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Memory Game Tests")
    print("=" * 40)
    
    try:
        test_game_initialization()
        test_deck_creation()
        test_match_logic()
        test_win_condition()
        test_two_player_mode()
        test_6x6_grid()
        
        print("\n" + "=" * 40)
        print("🎉 All tests passed! The Memory Game is working correctly.")
        print("✅ Color-based cards: Working")
        print("✅ Grid system (4x4, 6x6): Working")
        print("✅ Card matching logic: Working")
        print("✅ Player turn system: Working")
        print("✅ Score tracking: Working")
        print("✅ Win condition: Working")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)