#!/usr/bin/env python3
"""
Memory Game Demo Script
Demonstrates the memory game functionality automatically
"""

import requests
import random
import time

class MemoryGameDemo:
    def __init__(self):
        self.countries = [
            {"name": "United States", "code": "US"},
            {"name": "Canada", "code": "CA"}, 
            {"name": "United Kingdom", "code": "GB"},
            {"name": "France", "code": "FR"},
            {"name": "Germany", "code": "DE"},
            {"name": "Italy", "code": "IT"},
            {"name": "Spain", "code": "ES"},
            {"name": "Brazil", "code": "BR"}
        ]
        
    def test_api_connection(self):
        """Test the flagsapi.com connection"""
        print("🚀 Memory Game Demo - Countries Theme")
        print("=" * 50)
        print()
        
        print("Testing flagsapi.com connection...")
        try:
            response = requests.get("https://flagsapi.com/US/flat/64.png", timeout=5)
            if response.status_code == 200:
                print("✅ API connection successful!")
                print("   Flag images are available from flagsapi.com")
                return True
            else:
                print("⚠️  API returned status:", response.status_code)
                return False
        except Exception as e:
            print("⚠️  API connection failed:", str(e))
            print("   Game will work with country names instead")
            return False
            
    def demo_game_setup(self):
        """Demonstrate game setup"""
        print("\n🎮 Game Setup Demo")
        print("-" * 30)
        
        # Demo different grid sizes
        grid_options = [
            (4, "4x4 (16 cards, 8 pairs)"),
            (6, "6x6 (36 cards, 18 pairs)"), 
            (8, "8x8 (64 cards, 32 pairs)")
        ]
        
        print("Available grid sizes:")
        for size, description in grid_options:
            print(f"   {description}")
            
        print("\nPlayer options:")
        print("   1 Player - Solo challenge")
        print("   2 Players - Competitive mode")
        
        return 4  # Return 4x4 for demo
        
    def demo_board_creation(self, grid_size):
        """Demonstrate board creation"""
        print(f"\n🃏 Creating {grid_size}x{grid_size} Board")
        print("-" * 30)
        
        total_cards = grid_size * grid_size
        num_pairs = total_cards // 2
        
        print(f"Total cards needed: {total_cards}")
        print(f"Number of pairs: {num_pairs}")
        
        # Select countries for demo
        selected_countries = random.sample(self.countries, min(num_pairs, len(self.countries)))
        print(f"Selected countries: {[c['name'] for c in selected_countries]}")
        
        # Create pairs
        card_data = []
        for country in selected_countries:
            card_data.extend([country, country])
            
        # Show before shuffle
        print("\nBefore shuffle:")
        for i, country in enumerate(card_data):
            print(f"   Card {i+1}: {country['name']}")
            
        # Shuffle
        random.shuffle(card_data)
        print("\nAfter shuffle: (positions randomized)")
        
        # Create board
        board = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                card_index = i * grid_size + j
                if card_index < len(card_data):
                    row.append(card_data[card_index])
                else:
                    row.append(None)
            board.append(row)
            
        return board
        
    def demo_gameplay(self, board, grid_size):
        """Demonstrate gameplay mechanics"""
        print(f"\n🎯 Gameplay Demo")
        print("-" * 30)
        
        # Initialize game state
        revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        matched_pairs = set()
        score = 0
        
        print("Initial board (all cards hidden):")
        self.print_demo_board(board, revealed, grid_size)
        
        # Demo a few turns
        turns = [
            ((0, 0), (0, 1), "No match - different countries"),
            ((1, 0), (1, 1), "Match found!"),
            ((0, 2), (2, 0), "No match - different countries"),
            ((0, 0), (2, 2), "Match found!")
        ]
        
        for turn_num, (pos1, pos2, result) in enumerate(turns, 1):
            print(f"\nTurn {turn_num}:")
            row1, col1 = pos1
            row2, col2 = pos2
            
            if (row1 >= grid_size or col1 >= grid_size or 
                row2 >= grid_size or col2 >= grid_size or
                board[row1][col1] is None or board[row2][col2] is None):
                continue
                
            print(f"   Player chooses: ({row1+1},{col1+1}) and ({row2+1},{col2+1})")
            print(f"   Card 1: {board[row1][col1]['name']}")
            print(f"   Card 2: {board[row2][col2]['name']}")
            
            # Check for match
            if board[row1][col1]['code'] == board[row2][col2]['code']:
                print(f"   ✅ {result}")
                revealed[row1][col1] = True
                revealed[row2][col2] = True
                matched_pairs.add(board[row1][col1]['code'])
                score += 1
            else:
                print(f"   ❌ {result}")
                
            print(f"   Score: {score} pairs matched")
            self.print_demo_board(board, revealed, grid_size)
            
    def print_demo_board(self, board, revealed, grid_size):
        """Print board state for demo"""
        print("\n   Current board state:")
        
        # Column headers
        print("      ", end="")
        for j in range(grid_size):
            print(f"{j+1:>4}", end="")
        print()
        
        # Board rows
        for i in range(grid_size):
            print(f"   {i+1:>2} ", end="")
            for j in range(grid_size):
                if board[i][j] is None:
                    print("   -", end="")
                elif revealed[i][j]:
                    country_name = board[i][j]['name'][:3].upper()
                    print(f"{country_name:>4}", end="")
                else:
                    print("   ?", end="")
            print()
        print()
        
    def demo_api_features(self):
        """Demonstrate API integration features"""
        print("\n🌐 API Integration Features")
        print("-" * 30)
        
        print("flagsapi.com provides:")
        print("   📍 Country flag images")
        print("   🏷️  Standard country codes (ISO 3166-1)")
        print("   🖼️  Multiple flag formats and sizes")
        
        sample_urls = [
            "https://flagsapi.com/US/flat/64.png",
            "https://flagsapi.com/FR/shiny/64.png", 
            "https://flagsapi.com/GB/shiny/32.png"
        ]
        
        print("\nSample flag URLs:")
        for url in sample_urls:
            print(f"   {url}")
            
        print("\nGame integration:")
        print("   ✓ Country codes used for match validation")
        print("   ✓ Country names displayed as card labels")
        print("   ✓ API connectivity tested at startup")
        print("   ✓ Graceful fallback if API unavailable")
        
    def run_demo(self):
        """Run the complete demonstration"""
        # Test API
        api_available = self.test_api_connection()
        
        # Demo setup
        grid_size = self.demo_game_setup()
        
        # Demo board creation
        board = self.demo_board_creation(grid_size)
        
        # Demo gameplay
        self.demo_gameplay(board, grid_size)
        
        # Demo API features
        self.demo_api_features()
        
        print("\n🎉 Demo Complete!")
        print("=" * 50)
        print("To play the interactive game, run:")
        print("   python console_memory_game.py")
        print()
        print("Features demonstrated:")
        print("   ✓ Grid creation and card shuffling")
        print("   ✓ Memory game mechanics")
        print("   ✓ Match detection")
        print("   ✓ Score tracking")
        print("   ✓ API integration")
        print("   ✓ Country theme implementation")

def main():
    """Run the memory game demonstration"""
    demo = MemoryGameDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()