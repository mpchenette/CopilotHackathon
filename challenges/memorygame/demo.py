#!/usr/bin/env python3
"""
Demo script for Memory Game
Shows an automated playthrough to demonstrate game functionality
"""

import sys
import os
import time
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_game_console import MemoryGame

def simulate_game_demo():
    """Run a demonstration of the memory game"""
    print("🎮 Memory Game - Automated Demo")
    print("=" * 50)
    print("This demo shows the Memory Game in action!")
    print("Simulating a quick game to demonstrate functionality...\n")
    
    # Create and configure game
    game = MemoryGame()
    game.num_players = 1
    game.grid_size = 4
    game.total_cards = 16
    game.total_pairs = 8
    game.create_deck()
    game.game_active = True
    game.current_player = 1
    game.player_scores = [0, 0]
    
    print("Game Configuration:")
    print(f"- Grid Size: {game.grid_size}×{game.grid_size}")
    print(f"- Total Cards: {game.total_cards}")
    print(f"- Total Pairs: {game.total_pairs}")
    print(f"- Players: {game.num_players}")
    print()
    
    # Show initial board
    print("Initial Board (all cards face down):")
    game.display_board()
    
    print("\nColor Legend:")
    colors_used = set()
    for row in game.cards:
        for card in row:
            colors_used.add(card)
    
    for i, color_code in enumerate(sorted(colors_used)):
        color_name, color_ansi = game.colors[color_code]
        print(f"{color_ansi}{color_code}-{color_name}{game.reset_color}", end="  ")
        if (i + 1) % 4 == 0:
            print()
    print("\n")
    
    # Create a solution map for demo
    solution_map = {}
    for row in range(game.grid_size):
        for col in range(game.grid_size):
            color = game.cards[row][col]
            if color not in solution_map:
                solution_map[color] = []
            solution_map[color].append((row, col))
    
    # Simulate game turns
    turn = 1
    matches_found = 0
    
    print("🎯 Starting automated gameplay demonstration...")
    print("-" * 50)
    
    for color, positions in solution_map.items():
        if len(positions) == 2:
            pos1, pos2 = positions
            
            print(f"\nTurn {turn}: Looking for {game.colors[color][0]} pairs")
            print(f"Selecting position ({pos1[0]+1},{pos1[1]+1})...")
            
            # Reveal first card
            game.revealed[pos1[0]][pos1[1]] = True
            time.sleep(0.5)
            
            print(f"Found: {game.colors[color][1]}{game.colors[color][0]}{game.reset_color}")
            
            print(f"Selecting position ({pos2[0]+1},{pos2[1]+1})...")
            
            # Reveal second card
            game.revealed[pos2[0]][pos2[1]] = True
            time.sleep(0.5)
            
            print(f"Found: {game.colors[color][1]}{game.colors[color][0]}{game.reset_color}")
            
            # Check match
            is_match = game.check_match(pos1, pos2)
            matches_found += 1
            
            # Show current board state
            print("\nCurrent Board State:")
            game.display_board()
            print(f"Pairs matched: {matches_found}/{game.total_pairs}")
            
            turn += 1
            time.sleep(1)
            
            if matches_found >= game.total_pairs:
                break
    
    print("\n" + "=" * 50)
    print("🎊 DEMO COMPLETE! 🎊")
    print("The automated player successfully matched all pairs!")
    print(f"Total turns: {turn - 1}")
    print(f"Final score: {matches_found}/{game.total_pairs} pairs")
    
    # Show final board
    print("\nFinal Board (all cards matched):")
    game.display_board()
    
    print("\n✨ Game Features Demonstrated:")
    print("✅ Color-based cards with visual representation")
    print("✅ Grid layout and coordinate system") 
    print("✅ Card flipping and revealing mechanics")
    print("✅ Match detection and scoring")
    print("✅ Game state tracking")
    print("✅ Win condition detection")
    
    print(f"\n🎮 To play interactively, run: python3 memory_game_console.py")

def show_game_statistics():
    """Show some interesting statistics about the game"""
    print("\n📊 Memory Game Statistics:")
    print("-" * 30)
    
    # 4x4 grid stats
    cards_4x4 = 16
    pairs_4x4 = 8
    max_turns_4x4 = (cards_4x4 * (cards_4x4 - 1)) // 2  # Worst case scenario
    
    print(f"4×4 Grid:")
    print(f"  - Total cards: {cards_4x4}")
    print(f"  - Pairs to match: {pairs_4x4}")
    print(f"  - Minimum turns to win: {pairs_4x4}")
    print(f"  - Maximum possible turns: {max_turns_4x4}")
    
    # 6x6 grid stats  
    cards_6x6 = 36
    pairs_6x6 = 18
    max_turns_6x6 = (cards_6x6 * (cards_6x6 - 1)) // 2
    
    print(f"\n6×6 Grid:")
    print(f"  - Total cards: {cards_6x6}")
    print(f"  - Pairs to match: {pairs_6x6}")
    print(f"  - Minimum turns to win: {pairs_6x6}")
    print(f"  - Maximum possible turns: {max_turns_6x6}")
    
    print(f"\n🧠 Memory Challenge:")
    print(f"  - In 4×4: Remember positions of up to 8 different colors")
    print(f"  - In 6×6: Remember positions of up to 18 different colors")

if __name__ == "__main__":
    try:
        simulate_game_demo()
        show_game_statistics()
        
        print("\n" + "=" * 50)
        print("Demo completed successfully! 🎉")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")
        sys.exit(1)