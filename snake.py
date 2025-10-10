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
        self.root.resizable(False, False)
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.running = False
        self.started = False
        self.paused = False
        self.score = 0
        self.speed = 100
        self.high_score = self.load_high_score()
        
        # 🎵 Initialize pygame mixer
        pygame.mixer.init()
        self.load_sounds()
        
        # Create main frame
        main_frame = tk.Frame(root, bg="#2c3e50")
        main_frame.pack(padx=10, pady=10)
        
        # Info panel
        info_frame = tk.Frame(main_frame, bg="#34495e", padx=10, pady=5)
        info_frame.pack(fill=tk.X)
        
        self.score_label = tk.Label(info_frame, text="Score: 0", font=("Arial", 14, "bold"), 
                                     bg="#34495e", fg="#ecf0f1")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.high_score_label = tk.Label(info_frame, text=f"High Score: {self.high_score}", 
                                          font=("Arial", 14, "bold"), bg="#34495e", fg="#f39c12")
        self.high_score_label.pack(side=tk.LEFT, padx=10)
        
        self.level_label = tk.Label(info_frame, text="Level: 1", font=("Arial", 14, "bold"), 
                                     bg="#34495e", fg="#3498db")
        self.level_label.pack(side=tk.RIGHT, padx=10)
        
        # Canvas
        self.canvas = tk.Canvas(main_frame, width=self.width, height=self.height, 
                                bg="#d1f7c4", highlightthickness=2, highlightbackground="#2c3e50")
        self.canvas.pack()
        
        # Control hints
        hints_frame = tk.Frame(main_frame, bg="#34495e", padx=10, pady=5)
        hints_frame.pack(fill=tk.X)
        
        tk.Label(hints_frame, text="Controls: Arrow Keys to Move | P to Pause | R to Restart", 
                 font=("Arial", 10), bg="#34495e", fg="#95a5a6").pack()
        
        self.root.bind("<Key>", self.key_pressed)
        
        # Draw start screen
        self.draw_start_screen()
    
    # 🔊 Load sounds
    def load_sounds(self):
        try:
            self.eat_sound = pygame.mixer.Sound("eat.mp3")
            self.gameover_sound = pygame.mixer.Sound("gameover.mp3")
        except:
            self.eat_sound = None
            self.gameover_sound = None
    
    # 📀 Play sound helper
    def play_sound(self, sound):
        if sound:
            pygame.mixer.Sound.play(sound)
    
    def play_music(self):
        try:
            pygame.mixer.music.play(-1)
        except:
            pass
    
    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def draw_start_screen(self):
        self.canvas.delete("all")
        
        # Gradient-like background
        for i in range(20):
            color = f"#{200 - i * 3:02x}{247 - i * 2:02x}{196 - i:02x}"
            self.canvas.create_rectangle(0, i * 20, self.width, (i + 1) * 20, 
                                          fill=color, outline="")
        
        # Title with shadow
        self.canvas.create_text(self.width // 2 + 2, self.height // 2 - 78,
                                text="🐍 SNAKE GAME 🐍", font=("Arial", 32, "bold"), fill="#2c3e50")
        self.canvas.create_text(self.width // 2, self.height // 2 - 80,
                                text="🐍 SNAKE GAME 🐍", font=("Arial", 32, "bold"), fill="#27ae60")
        
        # Instructions box
        box_width = 400
        box_height = 180
        box_x = (self.width - box_width) // 2
        box_y = self.height // 2 - 30
        
        self.canvas.create_rectangle(box_x, box_y, box_x + box_width, box_y + box_height,
                                      fill="#ffffff", outline="#27ae60", width=3)
        
        self.canvas.create_text(self.width // 2, box_y + 30,
                                text="🎮 HOW TO PLAY 🎮", font=("Arial", 18, "bold"), fill="#27ae60")
        
        instructions = [
            "• Use Arrow Keys to control the snake",
            "• Eat red food to grow and score points",
            "• Avoid walls and your own tail",
            "• Every 50 points increases the speed!",
            "• Press P to pause during game"
        ]
        
        for i, instruction in enumerate(instructions):
            self.canvas.create_text(self.width // 2, box_y + 60 + i * 22,
                                    text=instruction, font=("Arial", 11), fill="#2c3e50")
        
        # Animated prompt
        self.canvas.create_text(self.width // 2, self.height - 40,
                                text="▶ PRESS ANY KEY TO START ◀", 
                                font=("Arial", 16, "bold"), fill="#e74c3c",
                                tags="blink")
        
        self.canvas.create_text(self.width // 2, self.height - 15,
                                text=f"🏆 High Score: {self.high_score} 🏆", 
                                font=("Arial", 13, "bold"), fill="#f39c12")
        
        # Animate the start prompt
        self.blink_prompt()
    
    def blink_prompt(self):
        if not self.started:
            try:
                current_color = self.canvas.itemcget("blink", "fill")
                new_color = "#e74c3c" if current_color == "#c0392b" else "#c0392b"
                self.canvas.itemconfig("blink", fill=new_color)
                self.root.after(500, self.blink_prompt)
            except:
                pass
    
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
        self.next_direction = "Right"
        self.running = True
        self.paused = False
        self.score = 0
        self.speed = 100
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = None
        self.create_food()
        self.update_labels()
        self.play_music()
        self.update_game()
    
    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")
        level = (self.score // 50) + 1
        self.level_label.config(text=f"Level: {level}")
    
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
        
        if key in ["p", "P"] and self.running:
            self.paused = not self.paused
            if self.paused:
                self.draw_pause_screen()
            return
        
        if key == "Up" and self.direction != "Down":
            self.next_direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.next_direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.next_direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.next_direction = "Right"
        elif key in ["r", "R"]:
            if not self.running:
                self.started = False
                self.draw_start_screen()
                self.root.after(100, lambda: setattr(self, 'started', False))
    
    def draw_pause_screen(self):
        # Semi-transparent overlay
        self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                      fill="#000000", stipple="gray50", tags="pause")
        self.canvas.create_text(self.width // 2, self.height // 2 - 20,
                                text="⏸ PAUSED ⏸", font=("Arial", 40, "bold"), 
                                fill="#ffffff", tags="pause")
        self.canvas.create_text(self.width // 2, self.height // 2 + 30,
                                text="Press P to Resume", font=("Arial", 16), 
                                fill="#ecf0f1", tags="pause")
    
    def move_snake(self):
        self.direction = self.next_direction
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
            self.update_labels()
            
            # Speed increase every 50 points
            if self.score % 50 == 0 and self.speed > 40:
                self.speed -= 10
            
            self.create_food()
        else:
            self.snake.pop()
    
    def change_background(self):
        colors = ["#d1f7c4", "#a1eafb", "#ffcbcb", "#f9f871", "#e8daff"]
        level = (self.score // 50) % len(colors)
        self.canvas.config(bg=colors[level])
    
    def update_game(self):
        if not self.running:
            return
        
        if self.paused:
            self.root.after(100, self.update_game)
            return
        
        self.canvas.delete("all")
        self.move_snake()
        self.change_background()
        
        # Draw grid (subtle)
        for i in range(0, self.width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.height, fill="#a0a0a0", dash=(1, 9))
        for i in range(0, self.height, self.cell_size):
            self.canvas.create_line(0, i, self.width, i, fill="#a0a0a0", dash=(1, 9))
        
        # Draw snake with gradient effect
        for i, (x, y) in enumerate(self.snake):
            if i == 0:  # Head
                # Draw eyes on head
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, 
                                              fill="#27ae60", outline="#1e8449", width=2)
                # Eyes based on direction
                if self.direction == "Right":
                    self.canvas.create_oval(x + 12, y + 4, x + 16, y + 8, fill="white", outline="black")
                    self.canvas.create_oval(x + 12, y + 12, x + 16, y + 16, fill="white", outline="black")
                elif self.direction == "Left":
                    self.canvas.create_oval(x + 4, y + 4, x + 8, y + 8, fill="white", outline="black")
                    self.canvas.create_oval(x + 4, y + 12, x + 8, y + 16, fill="white", outline="black")
                elif self.direction == "Up":
                    self.canvas.create_oval(x + 4, y + 4, x + 8, y + 8, fill="white", outline="black")
                    self.canvas.create_oval(x + 12, y + 4, x + 16, y + 8, fill="white", outline="black")
                else:  # Down
                    self.canvas.create_oval(x + 4, y + 12, x + 8, y + 16, fill="white", outline="black")
                    self.canvas.create_oval(x + 12, y + 12, x + 16, y + 16, fill="white", outline="black")
            else:  # Body
                intensity = 255 - (i * 10) if i * 10 < 100 else 155
                color = f"#{39:02x}{intensity:02x}{96:02x}"
                self.canvas.create_rectangle(x + 1, y + 1, x + self.cell_size - 1, 
                                              y + self.cell_size - 1, 
                                              fill=color, outline="#229954")
        
        # Draw food with animation
        fx, fy = self.food
        self.canvas.create_oval(fx + 2, fy + 2, fx + self.cell_size - 2, 
                                fy + self.cell_size - 2, 
                                fill="#e74c3c", outline="#c0392b", width=2)
        self.canvas.create_oval(fx + 6, fy + 6, fx + self.cell_size - 6, 
                                fy + self.cell_size - 6, 
                                fill="#ec7063")
        
        if self.running:
            self.root.after(self.speed, self.update_game)
        else:
            self.game_over()
    
    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.update_labels()
            new_record = True
        else:
            new_record = False
        
        # Semi-transparent overlay
        self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                      fill="#000000", stipple="gray50")
        
        # Game Over text with shadow
        self.canvas.create_text(self.width // 2 + 2, self.height // 2 - 58,
                                text="💀 GAME OVER 💀", font=("Arial", 36, "bold"), fill="#000000")
        self.canvas.create_text(self.width // 2, self.height // 2 - 60,
                                text="💀 GAME OVER 💀", font=("Arial", 36, "bold"), fill="#e74c3c")
        
        # Score box
        box_width = 300
        box_height = 120
        box_x = (self.width - box_width) // 2
        box_y = self.height // 2 - 20
        
        self.canvas.create_rectangle(box_x, box_y, box_x + box_width, box_y + box_height,
                                      fill="#ffffff", outline="#e74c3c", width=3)
        
        if new_record:
            self.canvas.create_text(self.width // 2, box_y + 25,
                                    text="🎉 NEW HIGH SCORE! 🎉", 
                                    font=("Arial", 16, "bold"), fill="#f39c12")
        
        self.canvas.create_text(self.width // 2, box_y + 55,
                                text=f"Your Score: {self.score}", 
                                font=("Arial", 20, "bold"), fill="#2c3e50")
        
        self.canvas.create_text(self.width // 2, box_y + 85,
                                text=f"High Score: {self.high_score}", 
                                font=("Arial", 14), fill="#7f8c8d")
        
        self.canvas.create_text(self.width // 2, self.height - 30,
                                text="Press R to Restart", 
                                font=("Arial", 16, "bold"), fill="#3498db")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()