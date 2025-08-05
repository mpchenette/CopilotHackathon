"""
Memory Game Implementation
A console-based memory game using colors as card symbols.
"""

import random
import time
import os


class MemoryGame:
    """A memory game with color-based cards."""
    
    COLORS = [
        "RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", 
        "PINK", "BROWN", "BLACK", "WHITE", "GRAY", "CYAN",
        "MAGENTA", "LIME", "NAVY", "MAROON", "OLIVE", "TEAL",
        "GOLD", "SILVER", "CORAL", "SALMON", "INDIGO", "VIOLET",
        "TAN", "BEIGE", "KHAKI", "AZURE", "IVORY", "CRIMSON",
        "SCARLET", "RUBY"
    ]
    
    def __init__(self, grid_size=4, num_players=1):
        """Initialize the memory game.
        
        Args:
            grid_size (int): Size of the grid (4, 6, or 8)
            num_players (int): Number of players (1 or 2)
        """
        if grid_size not in [4, 6, 8]:
            raise ValueError("Grid size must be 4, 6, or 8")
        if num_players not in [1, 2]:
            raise ValueError("Number of players must be 1 or 2")
            
        self.grid_size = grid_size
        self.num_players = num_players
        self.total_cards = grid_size * grid_size
        self.num_pairs = self.total_cards // 2
        
        # Game state
        self.cards = []
        self.revealed = []
        self.matched = []
        self.current_player = 1
        self.scores = [0] * num_players
        self.flipped_cards = []
        
        self._setup_game()
    
    def _setup_game(self):
        """Set up the game board with color pairs."""
        # Create pairs of colors
        colors_needed = self.num_pairs
        if colors_needed > len(self.COLORS):
            raise ValueError(f"Not enough colors for {self.grid_size}x{self.grid_size} grid")
        
        selected_colors = self.COLORS[:colors_needed]
        self.cards = selected_colors * 2  # Create pairs
        random.shuffle(self.cards)
        
        # Initialize game state
        self.revealed = [False] * self.total_cards
        self.matched = [False] * self.total_cards
        self.flipped_cards = []
    
    def display_board(self):
        """Display the current game board."""
        print("\n" + "="*50)
        print(f"MEMORY GAME - Player {self.current_player}'s Turn")
        if self.num_players == 2:
            print(f"Scores: Player 1: {self.scores[0]} | Player 2: {self.scores[1]}")
        else:
            print(f"Matches found: {self.scores[0]}")
        print("="*50)
        
        print("\n   ", end="")
        for col in range(self.grid_size):
            print(f"{col+1:3}", end="")
        print()
        
        for row in range(self.grid_size):
            print(f"{row+1:2} ", end="")
            for col in range(self.grid_size):
                index = row * self.grid_size + col
                if self.matched[index]:
                    print(f"{self.cards[index][:3]:3}", end="")
                elif self.revealed[index]:
                    print(f"{self.cards[index][:3]:3}", end="")
                else:
                    print(" ? ", end="")
            print()
        print()
    
    def get_card_position(self):
        """Get a valid card position from the player."""
        while True:
            try:
                user_input = input(f"Player {self.current_player}, enter row and column (e.g., '2 3') or 'quit': ").strip()
                if user_input.lower() == 'quit':
                    return None
                
                parts = user_input.split()
                if len(parts) != 2:
                    print("Please enter exactly two numbers separated by space (e.g., '2 3').")
                    continue
                    
                row, col = map(int, parts)
                if 1 <= row <= self.grid_size and 1 <= col <= self.grid_size:
                    index = (row - 1) * self.grid_size + (col - 1)
                    if not self.revealed[index] and not self.matched[index]:
                        return index
                    else:
                        print("That card is already revealed or matched. Try again.")
                else:
                    print(f"Please enter row and column between 1 and {self.grid_size}.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column separated by space (e.g., '2 3').")
    
    def flip_card(self, index):
        """Flip a card at the given index."""
        self.revealed[index] = True
        self.flipped_cards.append(index)
    
    def check_match(self):
        """Check if the two flipped cards match."""
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            if self.cards[card1] == self.cards[card2]:
                # Match found
                self.matched[card1] = True
                self.matched[card2] = True
                self.scores[self.current_player - 1] += 1
                print(f"\nMatch found! {self.cards[card1]} and {self.cards[card2]}")
                return True
            else:
                # No match
                print(f"\nNo match: {self.cards[card1]} and {self.cards[card2]}")
                time.sleep(2)  # Show cards briefly
                self.revealed[card1] = False
                self.revealed[card2] = False
                return False
        return False
    
    def switch_player(self):
        """Switch to the next player."""
        if self.num_players == 2:
            self.current_player = 2 if self.current_player == 1 else 1
    
    def is_game_over(self):
        """Check if the game is over (all pairs matched)."""
        return all(self.matched)
    
    def display_winner(self):
        """Display the game results."""
        print("\n" + "="*50)
        print("GAME OVER!")
        print("="*50)
        
        if self.num_players == 1:
            print(f"Congratulations! You found all {self.num_pairs} pairs!")
        else:
            if self.scores[0] > self.scores[1]:
                print("Player 1 wins!")
            elif self.scores[1] > self.scores[0]:
                print("Player 2 wins!")
            else:
                print("It's a tie!")
            print(f"Final scores: Player 1: {self.scores[0]} | Player 2: {self.scores[1]}")
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play(self):
        """Main game loop."""
        print("Welcome to the Memory Game!")
        print("Match pairs of colors by remembering their positions.")
        print("Enter row and column numbers to flip cards (e.g., '2 3').")
        print("Type 'quit' to exit the game.\n")
        
        while not self.is_game_over():
            self.display_board()
            
            # Player flips two cards
            for flip in range(2):
                if len(self.flipped_cards) < 2:
                    position = self.get_card_position()
                    if position is None:  # Player wants to quit
                        print("Thanks for playing!")
                        return
                    
                    self.flip_card(position)
                    self.display_board()
            
            # Check for match
            match_found = self.check_match()
            
            # Clear flipped cards
            self.flipped_cards = []
            
            # Switch player if no match (in 2-player mode)
            if not match_found:
                self.switch_player()
        
        self.display_winner()


def main():
    """Main function to set up and start the game."""
    print("Memory Game Setup")
    print("================")
    
    # Get grid size
    while True:
        try:
            grid_size = int(input("Choose grid size (4, 6, or 8): "))
            if grid_size in [4, 6, 8]:
                break
            else:
                print("Please choose 4, 6, or 8.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get number of players
    while True:
        try:
            num_players = int(input("Choose number of players (1 or 2): "))
            if num_players in [1, 2]:
                break
            else:
                print("Please choose 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Start the game
    game = MemoryGame(grid_size, num_players)
    game.play()


if __name__ == "__main__":
    main()