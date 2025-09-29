import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.running = True
        self.score = 0

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.root.bind("<Key>", self.key_pressed)

        self.start_game()

    def start_game(self):
        self.direction = "Right"
        self.running = True
        self.score = 0
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = None
        self.create_food()
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
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif key == "r" or key == "R":
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

        # Check collisions
        if (head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or new_head in self.snake):
            self.running = False
            return

        self.snake = [new_head] + self.snake

        # Check food
        if new_head == self.food:
            self.score += 10
            self.create_food()
        else:
            self.snake.pop()

    def update_game(self):
        self.canvas.delete("all")
        if self.running:
            self.move_snake()
            # Draw snake
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x+self.cell_size, y+self.cell_size, fill="green", outline="black")
            # Draw food
            fx, fy = self.food
            self.canvas.create_oval(fx, fy, fx+self.cell_size, fy+self.cell_size, fill="red")
            # Draw score
            self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", font=("Arial", 16), fill="black")
            self.root.after(100, self.update_game)
        else:
            self.canvas.create_text(self.width//2, self.height//2 - 20, text="Game Over!", font=("Arial", 32), fill="red")
            self.canvas.create_text(self.width//2, self.height//2 + 20, text=f"Score: {self.score}", font=("Arial", 24), fill="black")
            self.canvas.create_text(self.width//2, self.height//2 + 60, text="Press R to Restart", font=("Arial", 16), fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
