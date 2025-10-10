import tkinter as tk
import random
import os
try:
    import pygame
except ImportError:
    print("pygame is not installed. Please install it with 'pip install pygame'.")
    exit(1)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake Game by Prince")
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.running = False
        self.started = False
        self.score = 0
        self.speed = 100
        self.high_score = self.load_high_score()

        # 🎵 Initialize pygame mixer
        pygame.mixer.init()
        self.load_sounds()

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#d1f7c4")
        self.canvas.pack()

        self.root.bind("<Key>", self.key_pressed)

        # Draw start screen
        self.draw_start_screen()

    # 🔊 Load sounds
    def load_sounds(self):
        try:
            self.eat_sound = pygame.mixer.Sound("eat.mp3")
            self.gameover_sound = pygame.mixer.Sound("gameover.mp3")
            # pygame.mixer.music.load("bg_music.mp3")
        except:
            self.eat_sound = None
            self.gameover_sound = None

    # 📀 Play sound helper
    def play_sound(self, sound):
        if sound:
            pygame.mixer.Sound.play(sound)

    def play_music(self):
        try:
            pygame.mixer.music.play(-1)  # loop forever
        except:
            pass

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def draw_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.width // 2, self.height // 2 - 30,
                                text="🐍 Welcome to Snake Game 🐍", font=("Arial", 24, "bold"), fill="green")
        self.canvas.create_text(self.width // 2, self.height // 2 + 10,
                                text="Press any key to start", font=("Arial", 16), fill="blue")
        self.canvas.create_text(self.width // 2, self.height // 2 + 50,
                                text=f"High Score: {self.high_score}", font=("Arial", 14), fill="black")

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def start_game(self):
        self.direction = "Right"
        self.running = True
        self.score = 0
        self.speed = 100
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = None
        self.create_food()
        self.play_music()  # start background music
        self.update_game()

    def create_food(self):
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def key_pressed(self, event):
        key = event.keysym
        if not self.started:
            self.started = True
            self.start_game()
            return

        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif key in ["r", "R"]:
            if not self.running:
                self.start_game()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= self.cell_size
        elif self.direction == "Down":
            head_y += self.cell_size
        elif self.direction == "Left":
            head_x -= self.cell_size
        elif self.direction == "Right":
            head_x += self.cell_size

        new_head = (head_x, head_y)

        # Collision check
        if (head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or new_head in self.snake):
            self.running = False
            self.stop_music()
            self.play_sound(self.gameover_sound)
            return

        self.snake = [new_head] + self.snake

        # Food eaten
        if new_head == self.food:
            self.score += 10
            self.play_sound(self.eat_sound)
            if self.score % 50 == 0 and self.speed > 40:
                self.speed -= 10
            self.create_food()
        else:
            self.snake.pop()

    def change_background(self):
        colors = ["#d1f7c4", "#a1eafb", "#ffcbcb", "#f9f871"]
        level = (self.score // 50) % len(colors)
        self.canvas.config(bg=colors[level])

    def update_game(self):
        self.canvas.delete("all")
        if self.running:
            self.move_snake()
            self.change_background()
            # Draw snake
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="green", outline="black")
            # Draw food
            fx, fy = self.food
            self.canvas.create_oval(fx, fy, fx + self.cell_size, fy + self.cell_size, fill="red")
            # Draw score
            self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", font=("Arial", 14), fill="black")
            self.canvas.create_text(self.width - 10, 10, anchor="ne", text=f"High: {self.high_score}",
                                    font=("Arial", 14), fill="black")

            self.root.after(self.speed, self.update_game)
        else:
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.canvas.create_text(self.width // 2, self.height // 2 - 30, text="💀 Game Over 💀",
                                    font=("Arial", 32), fill="red")
            self.canvas.create_text(self.width // 2, self.height // 2 + 10, text=f"Score: {self.score}",
                                    font=("Arial", 20), fill="black")
            self.canvas.create_text(self.width // 2, self.height // 2 + 50, text="Press R to Restart",
                                    font=("Arial", 16), fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
