#!/usr/bin/env python3
"""
Memory Game - A color-based memory matching game (Console Version)
Created for the CopilotHackathon challenge

Game Rules:
- Grid of cards with colors hidden face down
- Players take turns selecting two card positions
- If cards match, they remain face up
- If cards don't match, they are hidden again
- Goal: Match all pairs to win the game

Features:
- 4x4 or 6x6 grid options
- 1-2 player support
- Color-based cards
- Console-based interface
"""

import random
import time
import os
import sys

class MemoryGame:
    def __init__(self):
        # Available colors with their display names
        self.colors = {
            'R': ('Red', '\033[91m'),
            'G': ('Green', '\033[92m'),
            'B': ('Blue', '\033[94m'),
            'Y': ('Yellow', '\033[93m'),
            'M': ('Magenta', '\033[95m'),
            'C': ('Cyan', '\033[96m'),
            'O': ('Orange', '\033[38;5;214m'),
            'P': ('Purple', '\033[35m'),
            'W': ('White', '\033[97m'),
            'L': ('Lime', '\033[38;5;46m'),
            'I': ('Indigo', '\033[38;5;54m'),
            'T': ('Teal', '\033[38;5;30m'),
            'S': ('Silver', '\033[37m'),
            'N': ('Navy', '\033[38;5;17m'),
            'K': ('Pink', '\033[38;5;213m'),
            'A': ('Aqua', '\033[38;5;51m'),
            'F': ('Forest', '\033[38;5;22m'),
            'V': ('Violet', '\033[38;5;129m')
        }
        
        self.reset_color = '\033[0m'
        
        # Game configuration
        self.grid_size = 4
        self.total_cards = 0
        self.total_pairs = 0
        
        # Game state
        self.cards = []
        self.revealed = []
        self.matched = []
        self.current_player = 1
        self.num_players = 1
        self.player_scores = [0, 0]
        self.game_active = False
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def setup_game(self):
        """Setup game configuration"""
        print("🎮 Welcome to Memory Game - Colors Edition! 🎨")
        print("=" * 50)
        
        # Choose number of players
        while True:
            try:
                self.num_players = int(input("Enter number of players (1 or 2): "))
                if self.num_players in [1, 2]:
                    break
                else:
                    print("Please enter 1 or 2")
            except ValueError:
                print("Please enter a valid number")
        
        # Choose grid size
        while True:
            grid_choice = input("Choose grid size (4 for 4x4, 6 for 6x6): ").strip()
            if grid_choice == '4':
                self.grid_size = 4
                break
            elif grid_choice == '6':
                self.grid_size = 6
                break
            else:
                print("Please enter 4 or 6")
        
        self.total_cards = self.grid_size * self.grid_size
        self.total_pairs = self.total_cards // 2
        
    def create_deck(self):
        """Create and shuffle the card deck"""
        # Get required number of colors
        color_keys = list(self.colors.keys())[:self.total_pairs]
        
        # Create pairs
        deck = color_keys * 2
        random.shuffle(deck)
        
        # Convert to 2D grid
        self.cards = []
        self.revealed = []
        self.matched = []
        
        for row in range(self.grid_size):
            card_row = []
            revealed_row = []
            matched_row = []
            
            for col in range(self.grid_size):
                index = row * self.grid_size + col
                card_row.append(deck[index])
                revealed_row.append(False)
                matched_row.append(False)
            
            self.cards.append(card_row)
            self.revealed.append(revealed_row)
            self.matched.append(matched_row)
    
    def display_board(self, show_positions=False):
        """Display the current game board"""
        print("\nCurrent Board:")
        print("=" * (self.grid_size * 6 + 1))
        
        # Column headers
        print("  ", end="")
        for col in range(self.grid_size):
            print(f"  {col+1}  ", end="")
        print()
        
        for row in range(self.grid_size):
            print(f"{row+1} ", end="")
            for col in range(self.grid_size):
                if self.matched[row][col]:
                    # Matched cards - show color
                    color_code = self.cards[row][col]
                    color_name, color_ansi = self.colors[color_code]
                    print(f"| {color_ansi}{color_code:^2}{self.reset_color} ", end="")
                elif self.revealed[row][col]:
                    # Currently revealed cards - show color
                    color_code = self.cards[row][col]
                    color_name, color_ansi = self.colors[color_code]
                    print(f"| {color_ansi}{color_code:^2}{self.reset_color} ", end="")
                else:
                    # Hidden cards
                    if show_positions:
                        print(f"| {row+1}{col+1} ", end="")
                    else:
                        print("|  ? ", end="")
            print("|")
        
        print("=" * (self.grid_size * 6 + 1))
        
        if show_positions:
            print("Position format: RC (Row Column)")
    
    def display_colors_legend(self):
        """Display the color legend"""
        print("\nColor Legend:")
        colors_per_row = 6
        color_items = list(self.colors.items())[:self.total_pairs]
        
        for i in range(0, len(color_items), colors_per_row):
            row_colors = color_items[i:i+colors_per_row]
            for code, (name, ansi) in row_colors:
                print(f"{ansi}{code}-{name}{self.reset_color}", end="  ")
            print()
    
    def get_player_input(self):
        """Get card selection from current player"""
        print(f"\nPlayer {self.current_player}'s turn")
        
        while True:
            try:
                pos_input = input("Enter card position (row,col) e.g., '2,3': ").strip()
                if ',' in pos_input:
                    row_str, col_str = pos_input.split(',')
                    row = int(row_str.strip()) - 1
                    col = int(col_str.strip()) - 1
                else:
                    # Allow format like "23" for row 2, col 3
                    if len(pos_input) == 2 and pos_input.isdigit():
                        row = int(pos_input[0]) - 1
                        col = int(pos_input[1]) - 1
                    else:
                        raise ValueError("Invalid format")
                
                # Validate position
                if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                    if not self.revealed[row][col] and not self.matched[row][col]:
                        return row, col
                    else:
                        print("Card already revealed or matched. Choose another.")
                else:
                    print(f"Position out of range. Use 1-{self.grid_size} for both row and column.")
                    
            except (ValueError, IndexError):
                print("Invalid input. Use format '2,3' or '23' for row 2, column 3")
    
    def reveal_card(self, row, col):
        """Reveal a card at given position"""
        self.revealed[row][col] = True
        color_code = self.cards[row][col]
        color_name, color_ansi = self.colors[color_code]
        print(f"Revealed: {color_ansi}{color_name}{self.reset_color} at position ({row+1},{col+1})")
    
    def check_match(self, pos1, pos2):
        """Check if two revealed cards match"""
        row1, col1 = pos1
        row2, col2 = pos2
        
        if self.cards[row1][col1] == self.cards[row2][col2]:
            # Match found!
            self.matched[row1][col1] = True
            self.matched[row2][col2] = True
            self.player_scores[self.current_player - 1] += 1
            
            color_code = self.cards[row1][col1]
            color_name, color_ansi = self.colors[color_code]
            print(f"\n🎉 MATCH! Both cards are {color_ansi}{color_name}{self.reset_color}!")
            
            return True
        else:
            # No match
            print("\n❌ No match. Cards will be hidden again.")
            time.sleep(2)
            
            self.revealed[row1][col1] = False
            self.revealed[row2][col2] = False
            
            return False
    
    def display_scores(self):
        """Display current scores"""
        if self.num_players == 1:
            matched_pairs = sum(sum(row) for row in self.matched) // 2
            print(f"\nPairs found: {matched_pairs}/{self.total_pairs}")
        else:
            print(f"\nScores - Player 1: {self.player_scores[0]} pairs | Player 2: {self.player_scores[1]} pairs")
    
    def check_win_condition(self):
        """Check if the game is won"""
        total_matched = sum(sum(row) for row in self.matched)
        return total_matched == self.total_cards
    
    def display_final_results(self):
        """Display final game results"""
        self.clear_screen()
        print("🎊 GAME OVER! 🎊")
        print("=" * 30)
        
        if self.num_players == 1:
            print("Congratulations! You matched all pairs!")
        else:
            print(f"Final Scores:")
            print(f"Player 1: {self.player_scores[0]} pairs")
            print(f"Player 2: {self.player_scores[1]} pairs")
            
            if self.player_scores[0] > self.player_scores[1]:
                print("🏆 Player 1 wins!")
            elif self.player_scores[1] > self.player_scores[0]:
                print("🏆 Player 2 wins!")
            else:
                print("🤝 It's a tie!")
        
        print("\nFinal board:")
        self.display_board()
    
    def play_turn(self):
        """Play one complete turn"""
        self.clear_screen()
        self.display_board()
        self.display_scores()
        
        # Get first card
        print("\nSelect first card:")
        pos1 = self.get_player_input()
        self.reveal_card(*pos1)
        
        self.clear_screen()
        self.display_board()
        
        # Get second card
        print("\nSelect second card:")
        pos2 = self.get_player_input()
        self.reveal_card(*pos2)
        
        self.clear_screen()
        self.display_board()
        
        # Check for match
        is_match = self.check_match(pos1, pos2)
        
        # Switch player if no match (in 2-player mode)
        if not is_match and self.num_players == 2:
            self.current_player = 3 - self.current_player
        
        input("\nPress Enter to continue...")
    
    def show_instructions(self):
        """Display game instructions"""
        print("\n📋 HOW TO PLAY:")
        print("1. Cards are arranged face down in a grid")
        print("2. Take turns selecting two cards by entering their positions")
        print("3. If the cards match, they remain face up and you score a point")
        print("4. If they don't match, they flip back face down")
        print("5. Goal: Match all pairs to win!")
        print("\n💡 TIP: Remember the positions of colors you've seen!")
        
        self.display_colors_legend()
        
        input("\nPress Enter to start the game...")
    
    def run(self):
        """Main game loop"""
        try:
            self.clear_screen()
            self.setup_game()
            self.create_deck()
            
            self.clear_screen()
            self.show_instructions()
            
            self.game_active = True
            self.current_player = 1
            self.player_scores = [0, 0]
            
            # Main game loop
            while self.game_active:
                self.play_turn()
                
                if self.check_win_condition():
                    self.game_active = False
                    self.display_final_results()
                    break
            
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try running the game again.")

def main():
    """Main function to start the game"""
    print("Starting Memory Game...")
    game = MemoryGame()
    game.run()

if __name__ == "__main__":
    main()