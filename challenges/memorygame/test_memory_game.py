#!/usr/bin/env python3
"""
Memory Game Test Script
Tests the core functionality of the memory game
"""

import sys
import os

# Add the current directory to path to import the game modules
sys.path.append(os.path.dirname(__file__))

from console_memory_game import ConsoleMemoryGame

def test_game_initialization():
    """Test game initialization"""
    print("Testing game initialization...")
    game = ConsoleMemoryGame()
    
    # Test initial state
    assert game.grid_size == 4, "Default grid size should be 4"
    assert game.num_players == 1, "Default players should be 1"
    assert game.current_player == 1, "Current player should start at 1"
    assert game.scores == [0, 0], "Scores should start at [0, 0]"
    assert not game.game_started, "Game should not be started initially"
    assert len(game.countries) > 0, "Countries list should not be empty"
    
    print("✅ Game initialization test passed")
    return True

def test_board_setup():
    """Test board setup functionality"""
    print("Testing board setup...")
    game = ConsoleMemoryGame()
    
    # Test different grid sizes
    for grid_size in [4, 6, 8]:
        game.grid_size = grid_size
        game.setup_board()
        
        # Verify board dimensions
        assert len(game.board) == grid_size, f"Board should have {grid_size} rows"
        assert len(game.board[0]) == grid_size, f"Board should have {grid_size} columns"
        
        # Verify revealed state
        assert len(game.revealed) == grid_size, f"Revealed matrix should have {grid_size} rows"
        assert len(game.revealed[0]) == grid_size, f"Revealed matrix should have {grid_size} columns"
        
        # Verify all cards are initially hidden
        for i in range(grid_size):
            for j in range(grid_size):
                assert not game.revealed[i][j], f"Card at ({i},{j}) should be initially hidden"
        
        # Verify correct number of pairs
        total_cards = grid_size * grid_size
        num_pairs = total_cards // 2
        card_counts = {}
        
        for i in range(grid_size):
            for j in range(grid_size):
                country_code = game.board[i][j]['code']
                card_counts[country_code] = card_counts.get(country_code, 0) + 1
        
        # Each country should appear exactly twice
        for country_code, count in card_counts.items():
            assert count == 2, f"Country {country_code} should appear exactly twice, found {count}"
        
        assert len(card_counts) == num_pairs, f"Should have {num_pairs} different countries"
    
    print("✅ Board setup test passed")
    return True

def test_country_data():
    """Test country data integrity"""
    print("Testing country data...")
    game = ConsoleMemoryGame()
    
    # Verify countries have required fields
    for country in game.countries:
        assert 'name' in country, "Country should have 'name' field"
        assert 'code' in country, "Country should have 'code' field"
        assert isinstance(country['name'], str), "Country name should be string"
        assert isinstance(country['code'], str), "Country code should be string"
        assert len(country['code']) == 2, "Country code should be 2 characters"
        assert country['code'].isupper(), "Country code should be uppercase"
    
    # Verify we have enough countries for largest grid
    max_pairs_needed = (8 * 8) // 2  # 32 pairs for 8x8 grid
    assert len(game.countries) >= max_pairs_needed, f"Need at least {max_pairs_needed} countries for 8x8 grid"
    
    print("✅ Country data test passed")
    return True

def test_game_logic():
    """Test basic game logic"""
    print("Testing game logic...")
    game = ConsoleMemoryGame()
    game.grid_size = 4
    game.setup_board()
    
    # Find two matching cards
    match_country = None
    positions = []
    
    for i in range(game.grid_size):
        for j in range(game.grid_size):
            country_code = game.board[i][j]['code']
            if match_country is None:
                match_country = country_code
                positions.append((i, j))
            elif country_code == match_country and len(positions) < 2:
                positions.append((i, j))
                break
        if len(positions) == 2:
            break
    
    # Test matching logic
    assert len(positions) == 2, "Should find two matching cards"
    
    pos1, pos2 = positions
    country1 = game.board[pos1[0]][pos1[1]]
    country2 = game.board[pos2[0]][pos2[1]]
    
    assert country1['code'] == country2['code'], "Matching cards should have same country code"
    
    print("✅ Game logic test passed")
    return True

def test_scoring():
    """Test scoring system"""
    print("Testing scoring system...")
    game = ConsoleMemoryGame()
    
    # Test single player scoring
    game.num_players = 1
    initial_score = game.scores[0]
    game.scores[0] += 1
    assert game.scores[0] == initial_score + 1, "Single player score should increment"
    
    # Test two player scoring
    game.num_players = 2
    game.scores = [0, 0]
    game.current_player = 1
    game.scores[game.current_player - 1] += 1
    assert game.scores[0] == 1, "Player 1 score should increment"
    assert game.scores[1] == 0, "Player 2 score should remain 0"
    
    game.current_player = 2
    game.scores[game.current_player - 1] += 1
    assert game.scores[0] == 1, "Player 1 score should remain 1"
    assert game.scores[1] == 1, "Player 2 score should increment"
    
    print("✅ Scoring system test passed")
    return True

def run_all_tests():
    """Run all tests"""
    print("🚀 Running Memory Game Tests")
    print("=" * 40)
    
    tests = [
        test_game_initialization,
        test_board_setup,
        test_country_data,
        test_game_logic,
        test_scoring
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("=" * 40)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"Total tests: {passed + failed}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

def main():
    """Main test function"""
    success = run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())