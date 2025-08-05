"""
Demo script to test the Memory Game functionality.
"""

from memory_game import MemoryGame


def demo_game():
    """Demonstrate the memory game functionality."""
    print("Memory Game Demo")
    print("===============")
    
    # Test 4x4 grid, single player
    print("\nCreating a 4x4 grid, single player game...")
    game = MemoryGame(4, 1)
    
    print(f"Game created successfully!")
    print(f"Grid size: {game.grid_size}x{game.grid_size}")
    print(f"Total cards: {game.total_cards}")
    print(f"Number of pairs: {game.num_pairs}")
    print(f"Players: {game.num_players}")
    
    # Show the initial board
    print("\nInitial board state:")
    game.display_board()
    
    # Demonstrate card flipping
    print("\nDemonstrating card flipping...")
    print(f"Card at position 0: {game.cards[0]}")
    print(f"Card at position 1: {game.cards[1]}")
    
    game.flip_card(0)
    game.flip_card(1)
    
    print("\nBoard after flipping cards 0 and 1:")
    game.display_board()
    
    # Check for match
    match_found = game.check_match()
    print(f"Match found: {match_found}")
    
    # Show final board state
    print("\nFinal board state:")
    game.display_board()
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    demo_game()