import tkinter as tk
from tkinter import messagebox
import random
import string
import time

class ChickenFarmSimulator:
    def __init__(self, root):
        # Set up the main game window
        self.root = root
        self.root.title("Chicken Farm Simulator")
        self.root.configure(bg="#f0f8ff")  # Light blue background

        # Initial game resources
        self.chickens = 2
        self.money = 100
        self.eggs = 0
        self.grass = 0
        self.water = 0
        self.game_over = False
        self.wolf_attack_interval = 3000  # 3 seconds in milliseconds

        # Create the GUI elements and display initial stats
        self.create_widgets()
        self.update_display()

        # Schedule the wolf attack
        self.schedule_wolf_attack()

    def create_widgets(self):
        # Label to show current game stats
        self.stats_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"), bg="#f0f8ff")
        self.stats_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons for player actions with appealing colors and fonts
        button_style = {"font": ("Arial", 10, "bold"), "bg": "#87ceeb", "fg": "white", "width": 20, "height": 2}

        self.plant_grass_button = tk.Button(self.root, text="Plant Grass (R5)", command=self.plant_grass, **button_style)
        self.plant_grass_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.buy_water_button = tk.Button(self.root, text="Buy Water (R3)", command=self.buy_water, **button_style)
        self.buy_water_button.grid(row=1, column=1, padx=5, pady=5)

        self.buy_chicken_button = tk.Button(self.root, text="Buy Chicken (R20)", command=self.buy_chicken, **button_style)
        self.buy_chicken_button.grid(row=2, column=0, padx=5, pady=5)

        self.produce_eggs_button = tk.Button(self.root, text="Produce Eggs", command=self.produce_eggs, **button_style)
        self.produce_eggs_button.grid(row=2, column=1, padx=5, pady=5)

        self.sell_eggs_button = tk.Button(self.root, text="Sell Eggs", command=self.sell_eggs, **button_style)
        self.sell_eggs_button.grid(row=3, column=0, padx=5, pady=5)

        # Entry field and label for wolf attack challenge with enhanced styles
        self.wolf_attack_label = tk.Label(self.root, text="", font=("Arial", 11, "italic"), bg="#f0f8ff", fg="red")
        self.wolf_attack_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.wolf_attack_entry = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.wolf_attack_entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.wolf_attack_entry.bind("<Return>", self.handle_wolf_attack)

    def update_display(self):
        # Update the stats label with current resources
        self.stats_label.config(
            text=f"Chickens: {self.chickens} | Money: R{self.money} | Eggs: {self.eggs} | Grass: {self.grass} | Water: {self.water}"
        )

    def plant_grass(self):
        # Decrease money and increase grass if affordable
        if self.money >= 5:
            self.money -= 5
            self.grass += 1
        self.update_display()

    def buy_water(self):
        # Decrease money and increase water if affordable
        if self.money >= 3:
            self.money -= 3
            self.water += 1
        self.update_display()

    def buy_chicken(self):
        # Decrease money and increase chickens if affordable
        if self.money >= 20:
            self.money -= 20
            self.chickens += 1
        self.update_display()

    def produce_eggs(self):
        # If there's grass and water, chickens produce eggs
        if self.grass > 0 and self.water > 0:
            self.eggs += self.chickens
            self.grass -= 1
            self.water -= 1
        self.update_display()

    def sell_eggs(self):
        # Sell all eggs and add money
        self.money += self.eggs * 2
        self.eggs = 0
        self.update_display()

    def schedule_wolf_attack(self):
        # Schedule the next wolf attack if the game is still running
        if not self.game_over:
            self.root.after(self.wolf_attack_interval, self.trigger_wolf_attack)

    def trigger_wolf_attack(self):
        # Display the wolf attack challenge, set a timer, and show an alert
        if not self.game_over:
            self.challenge_text = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            self.wolf_attack_label.config(text=f"A wolf is attacking! Type '{self.challenge_text}' to defend!")
            self.wolf_attack_entry.delete(0, tk.END)
            self.attack_start_time = time.time()
            self.schedule_wolf_attack()

    def handle_wolf_attack(self, event):
        # Check if the player correctly entered the challenge text in time (case-insensitive)
        user_input = self.wolf_attack_entry.get()
        if time.time() - self.attack_start_time <= 5 and user_input.lower() == self.challenge_text.lower():
            self.money += 10
            self.wolf_attack_label.config(text="You successfully defended against the wolf!")
        else:
            self.chickens = max(0, self.chickens - 1)
            self.wolf_attack_label.config(text="Oh no! A chicken was lost!")

        # Update display and clear the entry field
        self.update_display()
        self.wolf_attack_entry.delete(0, tk.END)

        # End game if no chickens remain
        if self.chickens == 0:
            self.end_game("All chickens are gone.")
            return

    def end_game(self, reason):
        # Display end game message with final stats
        self.game_over = True
        self.stats_label.config(
            text=f"Game Over! {reason}\nTotal Chickens: {self.chickens} | Eggs: {self.eggs} | Final Money: R{self.money}"
        )
        # Disable all action buttons
        for button in [self.plant_grass_button, self.buy_water_button, self.buy_chicken_button,
                       self.produce_eggs_button, self.sell_eggs_button]:
            button.config(state=tk.DISABLED)

# Start the game
root = tk.Tk()
game = ChickenFarmSimulator(root)
root.mainloop()
