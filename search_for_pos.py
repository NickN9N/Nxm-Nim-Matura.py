import tkinter as tk
from tkinter import messagebox
import random
import copy


class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid End Positions")

        self.label_width = tk.Label(self, text="Width:")
        self.label_width.grid(row=0, column=0)
        self.entry_width = tk.Entry(self)
        self.entry_width.grid(row=0, column=1)

        self.label_height = tk.Label(self, text="Height:")
        self.label_height.grid(row=1, column=0)
        self.entry_height = tk.Entry(self)
        self.entry_height.grid(row=1, column=1)

        self.button_generate = tk.Button(self, text="Generate Grid", command=self.generate_grid)
        self.button_generate.grid(row=2, column=0, columnspan=2)

        self.canvas = tk.Canvas(self, width=900, height=9000)
        self.canvas.grid(row=3, column=0, columnspan=2)

        self.grid = []
        self.grid_width = 10
        self.grid_height = 10
        self.cell_size = 20
        self.end_positions = set()

    def generate_grid(self):
        try:
            self.grid_width = int(self.entry_width.get())
            self.grid_height = int(self.entry_height.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for width and height.")
            return

        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.canvas.delete("all")

        self.find_end_positions()
        self.display_end_positions()

    def find_end_positions(self):
        self.end_positions = set()
        for _ in range(20):  # Generate multiple starting positions for more diversity
            start_x = random.randint(0, self.grid_width - 1)
            start_y = random.randint(0, self.grid_height - 1)
            initial_grid = copy.deepcopy(self.grid)
            initial_grid[start_y][start_x] = 1
            self.backtrack(initial_grid, start_x, start_y)

    def backtrack(self, grid, x, y):
        moves = self.get_possible_moves(grid, x, y)
        if not moves:
            self.end_positions.add(self.grid_to_tuple(grid))
            return
        for nx, ny in moves:
            new_grid = copy.deepcopy(grid)
            new_grid[ny][nx] = 1
            self.backtrack(new_grid, nx, ny)

    def get_possible_moves(self, grid, x, y):
        moves = []
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and grid[ny][nx] == 0:
                neighbors = sum((grid[ny + dy][nx + dx] == 1) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                                if 0 <= nx + dx < self.grid_width and 0 <= ny + dy < self.grid_height)
                if neighbors in [1, 3]:
                    moves.append((nx, ny))
        return moves

    def grid_to_tuple(self, grid):
        return tuple(tuple(row) for row in grid)

    def display_end_positions(self):
        self.canvas.delete("all")
        num_positions = len(self.end_positions)
        cols = int(self.canvas.winfo_width() // (self.grid_width * self.cell_size))
        rows = (num_positions + cols - 1) // cols

        gap = 10  # Gap between different positions

        for idx, grid in enumerate(self.end_positions):
            col = idx % cols
            row = idx // cols
            x_offset = col * (self.grid_width * self.cell_size + gap)
            y_offset = row * (self.grid_height * self.cell_size + gap)
            self.draw_grid(grid, x_offset, y_offset)

    def draw_grid(self, grid, x_offset, y_offset):
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.color_square(x, y, x_offset, y_offset)

    def color_square(self, x, y, x_offset, y_offset):
        x1, y1 = x * self.cell_size + x_offset, y * self.cell_size + y_offset
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="grey", outline="black")


if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
