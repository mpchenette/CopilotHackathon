#!/usr/bin/env python3
"""
Console Memory Game - Countries Theme
A console-based memory card matching game using country flags from flagsapi.com

Features:
- Grid sizes: 4x4, 6x6, 8x8
- 1-2 players support
- Country names as card symbols
- Type coordinates to flip cards
- Match pairs to win
"""

import requests
import random
import os
import time

class ConsoleMemoryGame:
    def __init__(self):
        # Game state
        self.grid_size = 4
        self.num_players = 1
        self.current_player = 1
        self.scores = [0, 0]  # Player 1, Player 2
        self.board = []
        self.revealed = []
        self.matched_pairs = set()
        self.game_started = False
        
        # Countries data
        self.countries = [
            {"name": "United States", "code": "US"},
            {"name": "Canada", "code": "CA"},
            {"name": "United Kingdom", "code": "GB"},
            {"name": "France", "code": "FR"},
            {"name": "Germany", "code": "DE"},
            {"name": "Italy", "code": "IT"},
            {"name": "Spain", "code": "ES"},
            {"name": "Brazil", "code": "BR"},
            {"name": "Japan", "code": "JP"},
            {"name": "Australia", "code": "AU"},
            {"name": "India", "code": "IN"},
            {"name": "China", "code": "CN"},
            {"name": "Russia", "code": "RU"},
            {"name": "Mexico", "code": "MX"},
            {"name": "Argentina", "code": "AR"},
            {"name": "South Africa", "code": "ZA"},
            {"name": "Egypt", "code": "EG"},
            {"name": "Nigeria", "code": "NG"},
            {"name": "South Korea", "code": "KR"},
            {"name": "Thailand", "code": "TH"},
            {"name": "Netherlands", "code": "NL"},
            {"name": "Sweden", "code": "SE"},
            {"name": "Norway", "code": "NO"},
            {"name": "Switzerland", "code": "CH"},
            {"name": "Austria", "code": "AT"},
            {"name": "Belgium", "code": "BE"},
            {"name": "Portugal", "code": "PT"},
            {"name": "Greece", "code": "GR"},
            {"name": "Turkey", "code": "TR"},
            {"name": "Poland", "code": "PL"},
            {"name": "Chile", "code": "CL"},
            {"name": "Peru", "code": "PE"}
        ]
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_title(self):
        """Print the game title"""
        print("=" * 50)
        print("    🃏 MEMORY GAME - COUNTRIES THEME 🃏")
        print("=" * 50)
        print()
        
    def get_game_settings(self):
        """Get game settings from user"""
        print("Game Settings:")
        print("-" * 20)
        
        # Grid size
        while True:
            try:
                print("Choose grid size:")
                print("1. 4x4 (16 cards)")
                print("2. 6x6 (36 cards)")
                print("3. 8x8 (64 cards)")
                choice = input("Enter choice (1-3): ").strip()
                
                if choice == "1":
                    self.grid_size = 4
                    break
                elif choice == "2":
                    self.grid_size = 6
                    break
                elif choice == "3":
                    self.grid_size = 8
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return False
                
        # Number of players
        while True:
            try:
                print("\nChoose number of players:")
                print("1. Single Player")
                print("2. Two Players")
                choice = input("Enter choice (1-2): ").strip()
                
                if choice == "1":
                    self.num_players = 1
                    break
                elif choice == "2":
                    self.num_players = 2
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return False
                
        return True
        
    def setup_board(self):
        """Setup the game board"""
        total_cards = self.grid_size * self.grid_size
        num_pairs = total_cards // 2
        
        # Select random countries for this game
        selected_countries = random.sample(self.countries, num_pairs)
        
        # Create pairs
        card_data = []
        for country in selected_countries:
            card_data.extend([country, country])  # Add each country twice for pairs
            
        # Shuffle the cards
        random.shuffle(card_data)
        
        # Create the board
        self.board = []
        self.revealed = []
        for i in range(self.grid_size):
            board_row = []
            revealed_row = []
            for j in range(self.grid_size):
                card_index = i * self.grid_size + j
                board_row.append(card_data[card_index])
                revealed_row.append(False)
            self.board.append(board_row)
            self.revealed.append(revealed_row)
            
        self.matched_pairs = set()
        self.scores = [0, 0]
        self.current_player = 1
        self.game_started = True
        
    def print_board(self, temp_revealed=None):
        """Print the current board state"""
        print(f"\nGrid Size: {self.grid_size}x{self.grid_size}")
        if self.num_players == 1:
            print(f"Pairs Found: {self.scores[0]}")
        else:
            print(f"Player 1: {self.scores[0]} pairs | Player 2: {self.scores[1]} pairs")
            print(f"Current Player: {self.current_player}")
        print()
        
        # Column headers
        print("   ", end="")
        for j in range(self.grid_size):
            print(f"{j+1:>4}", end="")
        print()
        
        # Board with row headers
        for i in range(self.grid_size):
            print(f"{i+1:>2} ", end="")
            for j in range(self.grid_size):
                if temp_revealed and temp_revealed[i][j]:
                    # Show temporarily revealed card
                    country_name = self.board[i][j]['name'][:3].upper()
                    print(f"{country_name:>4}", end="")
                elif self.revealed[i][j]:
                    # Show permanently revealed card
                    country_name = self.board[i][j]['name'][:3].upper()
                    print(f"{country_name:>4}", end="")
                else:
                    # Show hidden card
                    print("   ?", end="")
            print()
        print()
        
    def get_card_choice(self):
        """Get card choice from current player"""
        while True:
            try:
                if self.num_players == 2:
                    prompt = f"Player {self.current_player}, "
                else:
                    prompt = ""
                    
                choice = input(f"{prompt}enter row and column (e.g., '2 3') or 'quit': ").strip().lower()
                
                if choice == 'quit':
                    return None, None
                    
                parts = choice.split()
                if len(parts) != 2:
                    print("Please enter row and column separated by space (e.g., '2 3')")
                    continue
                    
                row = int(parts[0]) - 1  # Convert to 0-based index
                col = int(parts[1]) - 1  # Convert to 0-based index
                
                if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
                    print(f"Invalid coordinates. Use 1-{self.grid_size} for both row and column.")
                    continue
                    
                if self.revealed[row][col]:
                    print("This card is already revealed. Choose another.")
                    continue
                    
                return row, col
                
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column as numbers (e.g., '2 3')")
            except KeyboardInterrupt:
                print("\nGame cancelled.")
                return None, None
                
    def play_turn(self):
        """Play a single turn"""
        self.clear_screen()
        self.print_title()
        self.print_board()
        
        # Get first card
        print("Choose first card:")
        row1, col1 = self.get_card_choice()
        if row1 is None:
            return False  # Quit game
            
        # Show first card
        temp_revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        temp_revealed[row1][col1] = True
        
        self.clear_screen()
        self.print_title()
        self.print_board(temp_revealed)
        
        print(f"First card: {self.board[row1][col1]['name']}")
        print("\nChoose second card:")
        
        # Get second card
        row2, col2 = self.get_card_choice()
        if row2 is None:
            return False  # Quit game
            
        if row1 == row2 and col1 == col2:
            print("You can't choose the same card twice! Try again.")
            time.sleep(2)
            return True
            
        # Show both cards
        temp_revealed[row2][col2] = True
        
        self.clear_screen()
        self.print_title()
        self.print_board(temp_revealed)
        
        print(f"First card: {self.board[row1][col1]['name']}")
        print(f"Second card: {self.board[row2][col2]['name']}")
        
        # Check for match
        if self.board[row1][col1]['code'] == self.board[row2][col2]['code']:
            print("\n🎉 MATCH! 🎉")
            self.revealed[row1][col1] = True
            self.revealed[row2][col2] = True
            self.matched_pairs.add(self.board[row1][col1]['code'])
            self.scores[self.current_player - 1] += 1
            
            # Check for win
            if len(self.matched_pairs) == (self.grid_size * self.grid_size) // 2:
                self.game_won()
                return False
                
            print("You get another turn!")
        else:
            print("\n❌ No match. Cards will be hidden again.")
            if self.num_players == 2:
                self.current_player = 2 if self.current_player == 1 else 1
                print(f"Next player: Player {self.current_player}")
                
        input("\nPress Enter to continue...")
        return True
        
    def game_won(self):
        """Handle game win"""
        self.clear_screen()
        self.print_title()
        self.print_board()
        
        print("🏆 GAME OVER! 🏆")
        print("=" * 30)
        
        if self.num_players == 1:
            print(f"Congratulations! You found all {self.scores[0]} pairs!")
        else:
            print(f"Player 1: {self.scores[0]} pairs")
            print(f"Player 2: {self.scores[1]} pairs")
            
            if self.scores[0] > self.scores[1]:
                print("🥇 Player 1 wins!")
            elif self.scores[1] > self.scores[0]:
                print("🥇 Player 2 wins!")
            else:
                print("🤝 It's a tie!")
                
        print("\nThanks for playing!")
        
    def test_api_connection(self):
        """Test connection to flagsapi.com"""
        print("Testing connection to flagsapi.com...")
        try:
            response = requests.get("https://flagsapi.com/US/flat/64.png", timeout=5)
            if response.status_code == 200:
                print("✅ API connection successful!")
                print("Flag images are available from flagsapi.com")
            else:
                print("⚠️  API connection failed, but game will still work with country names.")
        except Exception as e:
            print("⚠️  API connection failed, but game will still work with country names.")
            print(f"Error: {e}")
        print()
        
    def run(self):
        """Run the memory game"""
        try:
            self.clear_screen()
            self.print_title()
            
            print("Welcome to the Memory Game!")
            print("Match pairs of countries to win.")
            print("Country data is themed around flags from flagsapi.com")
            print()
            
            # Test API connection
            self.test_api_connection()
            
            # Get game settings
            if not self.get_game_settings():
                return
                
            # Setup the game
            self.setup_board()
            
            print(f"\nStarting {self.grid_size}x{self.grid_size} game with {self.num_players} player(s)!")
            print("Enter coordinates as 'row column' (e.g., '2 3')")
            print("Type 'quit' to exit the game.")
            input("\nPress Enter to start...")
            
            # Main game loop
            while self.game_started:
                if not self.play_turn():
                    break
                    
        except KeyboardInterrupt:
            print("\n\nGame cancelled. Thanks for playing!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")

def main():
    """Main function to run the memory game"""
    game = ConsoleMemoryGame()
    game.run()

if __name__ == "__main__":
    main()