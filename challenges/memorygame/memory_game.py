#!/usr/bin/env python3
"""
Memory Game - Countries Theme
A memory card matching game using country flags from flagsapi.com

Features:
- Grid sizes: 4x4, 6x6, 8x8
- 1-2 players support
- Country flags as card symbols
- Click to flip cards
- Match pairs to win
"""

import tkinter as tk
from tkinter import messagebox, ttk
import requests
import random
import threading
from PIL import Image, ImageTk
import io
import time

class MemoryGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Game - Countries")
        self.root.geometry("800x600")
        
        # Game state
        self.grid_size = 4
        self.num_players = 1
        self.current_player = 1
        self.scores = [0, 0]  # Player 1, Player 2
        self.cards = []
        self.flipped_cards = []
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
        
        self.flag_images = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(self.root, text="Memory Game - Countries", 
                              font=("Arial", 24, "bold"))
        title_label.pack(pady=10)
        
        # Settings frame
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)
        
        # Grid size selection
        tk.Label(settings_frame, text="Grid Size:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.grid_var = tk.StringVar(value="4x4")
        grid_combo = ttk.Combobox(settings_frame, textvariable=self.grid_var, 
                                 values=["4x4", "6x6", "8x8"], width=8, state="readonly")
        grid_combo.pack(side=tk.LEFT, padx=5)
        
        # Number of players
        tk.Label(settings_frame, text="Players:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(20, 5))
        self.players_var = tk.StringVar(value="1")
        players_combo = ttk.Combobox(settings_frame, textvariable=self.players_var,
                                   values=["1", "2"], width=5, state="readonly")
        players_combo.pack(side=tk.LEFT, padx=5)
        
        # Start button
        start_btn = tk.Button(settings_frame, text="Start Game", 
                             command=self.start_game, font=("Arial", 12),
                             bg="#4CAF50", fg="white", padx=20)
        start_btn.pack(side=tk.LEFT, padx=20)
        
        # Score frame
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=10)
        
        self.score_label = tk.Label(self.score_frame, text="", font=("Arial", 14))
        self.score_label.pack()
        
        # Game board frame
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
    def start_game(self):
        """Start a new game"""
        self.grid_size = int(self.grid_var.get().split('x')[0])
        self.num_players = int(self.players_var.get())
        self.current_player = 1
        self.scores = [0, 0]
        self.flipped_cards = []
        self.matched_pairs = set()
        self.game_started = True
        
        # Clear previous board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
            
        self.update_score_display()
        self.create_game_board()
        
    def create_game_board(self):
        """Create the game board with cards"""
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
        
        # Create the grid
        self.cards = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                card_index = i * self.grid_size + j
                country = card_data[card_index]
                
                card_btn = tk.Button(self.board_frame, text="?", 
                                   font=("Arial", 16, "bold"),
                                   width=8, height=4,
                                   command=lambda r=i, c=j: self.flip_card(r, c),
                                   bg="#2196F3", fg="white")
                card_btn.grid(row=i, column=j, padx=2, pady=2)
                
                card = {
                    'button': card_btn,
                    'country': country,
                    'flipped': False,
                    'matched': False,
                    'row': i,
                    'col': j
                }
                row.append(card)
            self.cards.append(row)
            
        # Load flag images in background
        threading.Thread(target=self.load_flag_images, args=(selected_countries,), daemon=True).start()
        
    def load_flag_images(self, countries):
        """Load flag images from flagsapi.com"""
        for country in countries:
            try:
                # Use flagsapi.com to get flag image
                flag_url = f"https://flagsapi.com/{country['code']}/flat/64.png"
                response = requests.get(flag_url, timeout=5)
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    image = image.resize((60, 40), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.flag_images[country['code']] = photo
            except Exception as e:
                print(f"Failed to load flag for {country['name']}: {e}")
                # Fallback to country name if flag loading fails
                
    def flip_card(self, row, col):
        """Handle card flip"""
        if not self.game_started:
            return
            
        card = self.cards[row][col]
        
        # Don't flip if card is already flipped or matched
        if card['flipped'] or card['matched']:
            return
            
        # Don't allow more than 2 cards to be flipped at once
        if len(self.flipped_cards) >= 2:
            return
            
        # Flip the card
        card['flipped'] = True
        self.flipped_cards.append(card)
        
        # Update card display
        self.update_card_display(card)
        
        # Check for match if two cards are flipped
        if len(self.flipped_cards) == 2:
            self.root.after(1000, self.check_match)  # Delay to show both cards
            
    def update_card_display(self, card):
        """Update the visual display of a card"""
        if card['matched']:
            # Matched cards stay visible
            card['button'].config(text=card['country']['name'][:3].upper(), 
                                bg="#4CAF50", state=tk.DISABLED)
        elif card['flipped']:
            # Show country flag or name
            country_code = card['country']['code']
            if country_code in self.flag_images:
                card['button'].config(image=self.flag_images[country_code],
                                    text="", bg="white")
            else:
                card['button'].config(text=card['country']['name'][:3].upper(),
                                    bg="white", fg="black")
        else:
            # Hidden card
            card['button'].config(text="?", bg="#2196F3", fg="white", image="")
            
    def check_match(self):
        """Check if the two flipped cards match"""
        if len(self.flipped_cards) != 2:
            return
            
        card1, card2 = self.flipped_cards
        
        if card1['country']['code'] == card2['country']['code']:
            # Match found!
            card1['matched'] = True
            card2['matched'] = True
            self.matched_pairs.add(card1['country']['code'])
            
            # Update score
            self.scores[self.current_player - 1] += 1
            
            # Update card display
            self.update_card_display(card1)
            self.update_card_display(card2)
            
            # Check for win
            if len(self.matched_pairs) == (self.grid_size * self.grid_size) // 2:
                self.game_won()
            else:
                # Player gets another turn for a successful match
                pass
        else:
            # No match - flip cards back
            card1['flipped'] = False
            card2['flipped'] = False
            self.update_card_display(card1)
            self.update_card_display(card2)
            
            # Switch players if in 2-player mode
            if self.num_players == 2:
                self.current_player = 2 if self.current_player == 1 else 1
                
        # Clear flipped cards
        self.flipped_cards = []
        self.update_score_display()
        
    def update_score_display(self):
        """Update the score display"""
        if self.num_players == 1:
            score_text = f"Pairs Found: {self.scores[0]}"
        else:
            score_text = f"Player 1: {self.scores[0]} | Player 2: {self.scores[1]} | Current: Player {self.current_player}"
            
        self.score_label.config(text=score_text)
        
    def game_won(self):
        """Handle game win"""
        self.game_started = False
        
        if self.num_players == 1:
            message = f"Congratulations! You found all {self.scores[0]} pairs!"
        else:
            if self.scores[0] > self.scores[1]:
                message = f"Player 1 wins with {self.scores[0]} pairs!"
            elif self.scores[1] > self.scores[0]:
                message = f"Player 2 wins with {self.scores[1]} pairs!"
            else:
                message = f"It's a tie! Both players found {self.scores[0]} pairs!"
                
        messagebox.showinfo("Game Over", message)
        
    def run(self):
        """Start the game application"""
        self.root.mainloop()

def main():
    """Main function to run the memory game"""
    try:
        game = MemoryGame()
        game.run()
    except ImportError as e:
        print("Error: Missing required package.")
        print("Please install Pillow: pip install Pillow")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"Error starting game: {e}")

if __name__ == "__main__":
    main()