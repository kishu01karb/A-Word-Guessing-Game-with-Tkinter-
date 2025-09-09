import tkinter as tk
from tkinter import messagebox, font
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Hangman Game")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Hangman stages
        self.hangman_stages = [
            """
       ______
       |    |
       |    
       |    
       |    
       |    
    ___|___
            """,
            """
       ______
       |    |
       |    O
       |    
       |    
       |    
    ___|___
            """,
            """
       ______
       |    |
       |    O
       |    |
       |    
       |    
    ___|___
            """,
            """
       ______
       |    |
       |    O
       |   /|
       |    
       |    
    ___|___
            """,
            """
       ______
       |    |
       |    O
       |   /|\\
       |    
       |    
    ___|___
            """,
            """
       ______
       |    |
       |    O
       |   /|\\
       |   /
       |    
    ___|___
            """,
            """
       ______
       |    |
       |    O
       |   /|\\
       |   / \\
       |    
    ___|___
            """
        ]
        
        # Word bank
        self.word_bank = ['rizz', 'ohio', 'sigma', 'tiktok', 'skibidi', 'apple', 'ball', 'tree', 'book', 'fish', 
                         'gold', 'milk', 'rain', 'star', 'door', 'cake', 'frog', 'wolf', 'king', 'moon', 
                         'ship', 'road', 'fire', 'lake', 'rose', 'bird', 'home', 'nest', 'ring', 'farm', 
                         'play', 'jump', 'duck', 'goat', 'lamp', 'wind', 'sand', 'snow', 'leaf', 'seed', 
                         'pear', 'corn', 'wood', 'lock', 'bear', 'lion', 'cake', 'gift', 'shoe', 'soap', 
                         'sock', 'card', 'ball', 'kite', 'frog']
        
        # Game state
        self.current_word = ''
        self.guessed_word = []
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_over = False
        
        self.setup_ui()
        self.start_new_game()
        
    def setup_ui(self):
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(self.root, text="🎮 HANGMAN GAME 🎮", 
                              font=title_font, fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Hangman display frame
        hangman_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=3)
        hangman_frame.pack(pady=10, padx=20, fill='x')
        
        hangman_font = font.Font(family="Courier", size=12, weight="bold")
        self.hangman_label = tk.Label(hangman_frame, text="", font=hangman_font, 
                                     fg='#e74c3c', bg='#34495e', justify='left')
        self.hangman_label.pack(pady=15)
        
        # Word display frame
        word_frame = tk.Frame(self.root, bg='#3498db', relief='raised', bd=3)
        word_frame.pack(pady=10, padx=20, fill='x')
        
        word_font = font.Font(family="Arial", size=28, weight="bold")
        self.word_label = tk.Label(word_frame, text="", font=word_font, 
                                  fg='white', bg='#3498db')
        self.word_label.pack(pady=15)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#2c3e50')
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Enter a letter:", font=("Arial", 14, "bold"), 
                fg='#ecf0f1', bg='#2c3e50').pack()
        
        self.guess_entry = tk.Entry(input_frame, font=("Arial", 16), width=5, 
                                   justify='center', bg='#ecf0f1')
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind('<Return>', lambda event: self.make_guess())
        self.guess_entry.bind('<KeyRelease>', self.on_key_release)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        self.guess_button = tk.Button(button_frame, text="GUESS!", font=("Arial", 12, "bold"),
                                     bg='#e74c3c', fg='white', padx=20, pady=5,
                                     command=self.make_guess, relief='raised', bd=3)
        self.guess_button.pack(side='left', padx=10)
        
        new_game_button = tk.Button(button_frame, text="NEW GAME", font=("Arial", 12, "bold"),
                                   bg='#27ae60', fg='white', padx=20, pady=5,
                                   command=self.start_new_game, relief='raised', bd=3)
        new_game_button.pack(side='left', padx=10)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=20, fill='x')
        
        # Wrong guesses info
        wrong_frame = tk.Frame(info_frame, bg='#e74c3c', relief='raised', bd=2)
        wrong_frame.pack(side='left', padx=20, pady=5, fill='x', expand=True)
        
        tk.Label(wrong_frame, text="Wrong Guesses", font=("Arial", 12, "bold"),
                fg='white', bg='#e74c3c').pack(pady=5)
        self.wrong_label = tk.Label(wrong_frame, text="0 / 6", font=("Arial", 14, "bold"),
                                   fg='white', bg='#e74c3c')
        self.wrong_label.pack(pady=5)
        
        # Word length info
        length_frame = tk.Frame(info_frame, bg='#9b59b6', relief='raised', bd=2)
        length_frame.pack(side='right', padx=20, pady=5, fill='x', expand=True)
        
        tk.Label(length_frame, text="Word Length", font=("Arial", 12, "bold"),
                fg='white', bg='#9b59b6').pack(pady=5)
        self.length_label = tk.Label(length_frame, text="- letters", font=("Arial", 14, "bold"),
                                    fg='white', bg='#9b59b6')
        self.length_label.pack(pady=5)
        
        # Guessed letters frame
        guessed_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=3)
        guessed_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(guessed_frame, text="Guessed Letters:", font=("Arial", 12, "bold"),
                fg='#ecf0f1', bg='#34495e').pack(pady=5)
        
        self.guessed_label = tk.Label(guessed_frame, text="None", font=("Arial", 14),
                                     fg='#f39c12', bg='#34495e', wraplength=600)
        self.guessed_label.pack(pady=10)
        
        # Message label
        self.message_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"),
                                     fg='#2ecc71', bg='#2c3e50')
        self.message_label.pack(pady=10)
    
    def on_key_release(self, event):
        # Convert to lowercase and limit to single letter
        text = self.guess_entry.get().lower()
        if text and not text.isalpha():
            self.guess_entry.delete(0, tk.END)
        elif len(text) > 1:
            self.guess_entry.delete(1, tk.END)
        else:
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.insert(0, text)
    
    def start_new_game(self):
        self.current_word = random.choice(self.word_bank)
        self.guessed_word = ['_'] * len(self.current_word)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.game_over = False
        
        self.update_display()
        self.guess_entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.message_label.config(text="Good luck! Start guessing letters!", fg='#3498db')
        self.guess_entry.focus()
    
    def update_display(self):
        # Update hangman drawing
        self.hangman_label.config(text=self.hangman_stages[self.wrong_guesses])
        
        # Update word display
        self.word_label.config(text=' '.join(self.guessed_word))
        
        # Update wrong guesses
        self.wrong_label.config(text=f"{self.wrong_guesses} / {self.max_wrong_guesses}")
        
        # Update word length
        self.length_label.config(text=f"{len(self.current_word)} letters")
        
        # Update guessed letters
        if self.guessed_letters:
            letters_display = ', '.join([letter.upper() for letter in self.guessed_letters])
            self.guessed_label.config(text=letters_display)
        else:
            self.guessed_label.config(text="None")
    
    def make_guess(self):
        if self.game_over:
            return
            
        guess = self.guess_entry.get().lower().strip()
        
        # Validation
        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter!")
            self.guess_entry.focus()
            return
        
        if guess in self.guessed_letters:
            messagebox.showwarning("Already Guessed", "You already guessed that letter!")
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus()
            return
        
        self.guessed_letters.append(guess)
        
        if guess in self.current_word:
            # Correct guess
            for i in range(len(self.current_word)):
                if self.current_word[i] == guess:
                    self.guessed_word[i] = guess
            self.message_label.config(text=f"Great guess! '{guess.upper()}' is in the word!", fg='#2ecc71')
        else:
            # Wrong guess
            self.wrong_guesses += 1
            self.message_label.config(text=f"Sorry! '{guess.upper()}' is not in the word.", fg='#e74c3c')
        
        self.update_display()
        self.guess_entry.delete(0, tk.END)
        
        # Check win/lose conditions
        if '_' not in self.guessed_word:
            # Won!
            self.message_label.config(text=f"🎉 CONGRATULATIONS! You guessed '{self.current_word.upper()}'! 🎉", 
                                     fg='#f39c12')
            self.end_game()
            messagebox.showinfo("You Won!", f"Congratulations! You successfully guessed the word: {self.current_word.upper()}")
        elif self.wrong_guesses >= self.max_wrong_guesses:
            # Lost!
            self.message_label.config(text=f"💀 GAME OVER! The word was '{self.current_word.upper()}'", 
                                     fg='#e74c3c')
            self.end_game()
            messagebox.showinfo("Game Over", f"You've been hanged! The word was: {self.current_word.upper()}")
        else:
            self.guess_entry.focus()
    
    def end_game(self):
        self.game_over = True
        self.guess_entry.config(state='disabled')
        self.guess_button.config(state='disabled')

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()