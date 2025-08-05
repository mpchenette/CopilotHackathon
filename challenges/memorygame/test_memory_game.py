"""
Test file for the Memory Game implementation.
Basic tests to verify game functionality.
"""

import unittest
from memory_game import MemoryGame


class TestMemoryGame(unittest.TestCase):
    """Test cases for the Memory Game."""
    
    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        game = MemoryGame(4, 1)
        self.assertEqual(game.grid_size, 4)
        self.assertEqual(game.num_players, 1)
        self.assertEqual(game.total_cards, 16)
        self.assertEqual(game.num_pairs, 8)
        self.assertEqual(len(game.cards), 16)
        self.assertEqual(len(game.revealed), 16)
        self.assertEqual(len(game.matched), 16)
    
    def test_invalid_grid_size(self):
        """Test that invalid grid sizes raise ValueError."""
        with self.assertRaises(ValueError):
            MemoryGame(3, 1)  # Invalid grid size
        with self.assertRaises(ValueError):
            MemoryGame(5, 1)  # Invalid grid size
    
    def test_invalid_player_count(self):
        """Test that invalid player counts raise ValueError."""
        with self.assertRaises(ValueError):
            MemoryGame(4, 0)  # Invalid player count
        with self.assertRaises(ValueError):
            MemoryGame(4, 3)  # Invalid player count
    
    def test_card_pairs_creation(self):
        """Test that cards are created in pairs."""
        game = MemoryGame(4, 1)
        color_counts = {}
        for color in game.cards:
            color_counts[color] = color_counts.get(color, 0) + 1
        
        # Each color should appear exactly twice
        for count in color_counts.values():
            self.assertEqual(count, 2)
    
    def test_flip_card(self):
        """Test that flipping cards works correctly."""
        game = MemoryGame(4, 1)
        
        # Initially no cards should be revealed
        self.assertFalse(any(game.revealed))
        
        # Flip a card
        game.flip_card(0)
        self.assertTrue(game.revealed[0])
        self.assertEqual(len(game.flipped_cards), 1)
        self.assertEqual(game.flipped_cards[0], 0)
    
    def test_match_detection(self):
        """Test that match detection works correctly."""
        game = MemoryGame(4, 1)
        
        # Find two cards with the same color
        first_color = game.cards[0]
        second_index = -1
        for i in range(1, len(game.cards)):
            if game.cards[i] == first_color:
                second_index = i
                break
        
        # Flip both matching cards
        game.flip_card(0)
        game.flip_card(second_index)
        
        # Check match
        match_found = game.check_match()
        self.assertTrue(match_found)
        self.assertTrue(game.matched[0])
        self.assertTrue(game.matched[second_index])
        self.assertEqual(game.scores[0], 1)
    
    def test_no_match_detection(self):
        """Test that non-matching cards are handled correctly."""
        game = MemoryGame(4, 1)
        
        # Find two cards with different colors
        first_color = game.cards[0]
        second_index = -1
        for i in range(1, len(game.cards)):
            if game.cards[i] != first_color:
                second_index = i
                break
        
        # If we couldn't find different colors, skip this test
        if second_index == -1:
            self.skipTest("All cards have the same color (very unlikely)")
        
        # Flip both non-matching cards
        game.flip_card(0)
        game.flip_card(second_index)
        
        # Check match
        match_found = game.check_match()
        self.assertFalse(match_found)
        self.assertFalse(game.matched[0])
        self.assertFalse(game.matched[second_index])
        # Cards should be hidden again
        self.assertFalse(game.revealed[0])
        self.assertFalse(game.revealed[second_index])
    
    def test_game_over_condition(self):
        """Test that game over detection works correctly."""
        game = MemoryGame(4, 1)
        
        # Initially game should not be over
        self.assertFalse(game.is_game_over())
        
        # Mark all cards as matched
        for i in range(len(game.matched)):
            game.matched[i] = True
        
        # Now game should be over
        self.assertTrue(game.is_game_over())
    
    def test_player_switching(self):
        """Test that player switching works correctly in 2-player mode."""
        game = MemoryGame(4, 2)
        
        # Initially player 1
        self.assertEqual(game.current_player, 1)
        
        # Switch player
        game.switch_player()
        self.assertEqual(game.current_player, 2)
        
        # Switch again
        game.switch_player()
        self.assertEqual(game.current_player, 1)
    
    def test_different_grid_sizes(self):
        """Test that different grid sizes work correctly."""
        for grid_size in [4, 6, 8]:
            game = MemoryGame(grid_size, 1)
            expected_cards = grid_size * grid_size
            expected_pairs = expected_cards // 2
            
            self.assertEqual(len(game.cards), expected_cards)
            self.assertEqual(game.num_pairs, expected_pairs)
            self.assertEqual(len(game.revealed), expected_cards)
            self.assertEqual(len(game.matched), expected_cards)


if __name__ == "__main__":
    unittest.main()