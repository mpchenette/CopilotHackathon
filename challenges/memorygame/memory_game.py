#!/usr/bin/env python3
"""
Memory Game - A color-based memory matching game
Created for the CopilotHackathon challenge

Game Rules:
- Grid of cards with colors hidden face down
- Players take turns flipping two cards
- If cards match, they remain face up
- If cards don't match, they flip back after a short delay
- Goal: Match all pairs to win the game

Features:
- 4x4 grid (16 cards, 8 pairs)
- 1-2 player support
- Color-based cards
- Click-to-flip mechanics
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from threading import Timer

class MemoryGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Game - Colors")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Game configuration
        self.grid_size = 4  # 4x4 grid
        self.total_cards = self.grid_size * self.grid_size
        self.total_pairs = self.total_cards // 2
        
        # Color pairs for the cards
        self.colors = [
            '#FF0000', '#00FF00', '#0000FF', '#FFFF00',  # Red, Green, Blue, Yellow
            '#FF00FF', '#00FFFF', '#FFA500', '#800080'   # Magenta, Cyan, Orange, Purple
        ]
        
        # Game state
        self.cards = []
        self.card_buttons = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.current_player = 1
        self.num_players = 1
        self.player_scores = [0, 0]  # [Player 1, Player 2]
        self.game_active = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(self.root, text="Memory Game - Colors", 
                              font=("Arial", 20, "bold"), fg="#333")
        title_label.pack(pady=10)
        
        # Game setup frame
        setup_frame = tk.Frame(self.root)
        setup_frame.pack(pady=10)
        
        # Player selection
        tk.Label(setup_frame, text="Number of Players:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.player_var = tk.StringVar(value="1")
        player_combo = ttk.Combobox(setup_frame, textvariable=self.player_var, 
                                   values=["1", "2"], state="readonly", width=5)
        player_combo.grid(row=0, column=1, padx=5)
        
        # Grid size selection
        tk.Label(setup_frame, text="Grid Size:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.grid_var = tk.StringVar(value="4x4")
        grid_combo = ttk.Combobox(setup_frame, textvariable=self.grid_var,
                                 values=["4x4", "6x6"], state="readonly", width=5)
        grid_combo.grid(row=0, column=3, padx=5)
        grid_combo.bind("<<ComboboxSelected>>", self.on_grid_change)
        
        # Start button
        start_btn = tk.Button(setup_frame, text="Start New Game", 
                             command=self.start_new_game, 
                             font=("Arial", 12), bg="#4CAF50", fg="white")
        start_btn.grid(row=0, column=4, padx=10)
        
        # Game info frame
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)
        
        # Current player and scores
        self.info_label = tk.Label(self.info_frame, text="Click 'Start New Game' to begin", 
                                  font=("Arial", 12))
        self.info_label.pack()
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg="#f0f0f0", relief="raised", bd=2)
        self.board_frame.pack(pady=20, padx=20)
        
        # Initialize empty board
        self.create_board()
        
    def on_grid_change(self, event=None):
        """Handle grid size change"""
        grid_text = self.grid_var.get()
        if grid_text == "4x4":
            self.grid_size = 4
            self.colors = [
                '#FF0000', '#00FF00', '#0000FF', '#FFFF00',  # Red, Green, Blue, Yellow
                '#FF00FF', '#00FFFF', '#FFA500', '#800080'   # Magenta, Cyan, Orange, Purple
            ]
        elif grid_text == "6x6":
            self.grid_size = 6
            self.colors = [
                '#FF0000', '#00FF00', '#0000FF', '#FFFF00',  # Red, Green, Blue, Yellow
                '#FF00FF', '#00FFFF', '#FFA500', '#800080',  # Magenta, Cyan, Orange, Purple
                '#A52A2A', '#FFC0CB', '#90EE90', '#FFB6C1',  # Brown, Pink, Light Green, Light Pink
                '#DDA0DD', '#F0E68C', '#E6E6FA', '#F5DEB3',  # Plum, Khaki, Lavender, Wheat
                '#98FB98', '#F0F8FF'  # Pale Green, Alice Blue
            ]
        
        self.total_cards = self.grid_size * self.grid_size
        self.total_pairs = self.total_cards // 2
        self.create_board()
        
    def create_board(self):
        """Create the game board with empty cards"""
        # Clear existing board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.card_buttons = []
        
        # Create grid of buttons
        for row in range(self.grid_size):
            button_row = []
            for col in range(self.grid_size):
                btn = tk.Button(self.board_frame, 
                               text="?", 
                               width=8, 
                               height=4,
                               font=("Arial", 12, "bold"),
                               bg="#d3d3d3",
                               state="disabled",
                               command=lambda r=row, c=col: self.card_clicked(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.card_buttons.append(button_row)
    
    def start_new_game(self):
        """Start a new game"""
        self.num_players = int(self.player_var.get())
        self.current_player = 1
        self.player_scores = [0, 0]
        self.matched_pairs = 0
        self.flipped_cards = []
        self.game_active = True
        
        # Create card deck with color pairs
        card_colors = self.colors[:self.total_pairs] * 2  # Each color appears twice
        random.shuffle(card_colors)
        
        # Convert to 2D grid
        self.cards = []
        for row in range(self.grid_size):
            card_row = []
            for col in range(self.grid_size):
                index = row * self.grid_size + col
                card_row.append({
                    'color': card_colors[index],
                    'flipped': False,
                    'matched': False
                })
            self.cards.append(card_row)
        
        # Reset all buttons
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = self.card_buttons[row][col]
                btn.config(text="?", bg="#d3d3d3", state="normal")
                
        self.update_info()
        
    def card_clicked(self, row, col):
        """Handle card click"""
        if not self.game_active:
            return
            
        card = self.cards[row][col]
        
        # Can't click already flipped or matched cards
        if card['flipped'] or card['matched']:
            return
        
        # Can't flip more than 2 cards at a time
        if len(self.flipped_cards) >= 2:
            return
        
        # Flip the card
        card['flipped'] = True
        self.flipped_cards.append((row, col))
        
        # Update button appearance
        btn = self.card_buttons[row][col]
        btn.config(bg=card['color'], text="", state="disabled")
        
        # Check if we have 2 flipped cards
        if len(self.flipped_cards) == 2:
            self.root.after(1000, self.check_match)  # Wait 1 second before checking
            
    def check_match(self):
        """Check if the two flipped cards match"""
        if len(self.flipped_cards) != 2:
            return
            
        row1, col1 = self.flipped_cards[0]
        row2, col2 = self.flipped_cards[1]
        
        card1 = self.cards[row1][col1]
        card2 = self.cards[row2][col2]
        
        if card1['color'] == card2['color']:
            # Match found!
            card1['matched'] = True
            card2['matched'] = True
            self.matched_pairs += 1
            self.player_scores[self.current_player - 1] += 1
            
            # Keep cards visible but mark as matched
            self.card_buttons[row1][col1].config(relief="sunken")
            self.card_buttons[row2][col2].config(relief="sunken")
            
            # Check for win condition
            if self.matched_pairs == self.total_pairs:
                self.game_over()
        else:
            # No match - flip cards back
            card1['flipped'] = False
            card2['flipped'] = False
            
            self.card_buttons[row1][col1].config(bg="#d3d3d3", text="?", state="normal")
            self.card_buttons[row2][col2].config(bg="#d3d3d3", text="?", state="normal")
            
            # Switch player in 2-player mode
            if self.num_players == 2:
                self.current_player = 3 - self.current_player  # Switch between 1 and 2
        
        self.flipped_cards = []
        self.update_info()
        
    def update_info(self):
        """Update the game information display"""
        if not self.game_active:
            self.info_label.config(text="Click 'Start New Game' to begin")
            return
            
        if self.num_players == 1:
            info_text = f"Pairs found: {self.matched_pairs}/{self.total_pairs}"
        else:
            info_text = f"Current Player: {self.current_player} | "
            info_text += f"Player 1: {self.player_scores[0]} pairs | "
            info_text += f"Player 2: {self.player_scores[1]} pairs"
            
        self.info_label.config(text=info_text)
        
    def game_over(self):
        """Handle game over"""
        self.game_active = False
        
        if self.num_players == 1:
            messagebox.showinfo("Congratulations!", 
                               f"You won!\nYou matched all {self.total_pairs} pairs!")
        else:
            if self.player_scores[0] > self.player_scores[1]:
                winner = "Player 1"
            elif self.player_scores[1] > self.player_scores[0]:
                winner = "Player 2"
            else:
                winner = "It's a tie"
                
            messagebox.showinfo("Game Over!", 
                               f"{winner}!\n"
                               f"Player 1: {self.player_scores[0]} pairs\n"
                               f"Player 2: {self.player_scores[1]} pairs")
        
        # Disable all cards
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.card_buttons[row][col].config(state="disabled")
                
    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = MemoryGame()
    game.run()