import tkinter as tk
from tkinter import messagebox


def generate_grid():
    try:
        length = int(length_entry.get())
        width = int(width_entry.get())

        # Hide input widgets
        length_label.grid_forget()
        length_entry.grid_forget()
        width_label.grid_forget()
        width_entry.grid_forget()
        generate_button.grid_forget()

        # Generate the grid of buttons
        buttons = []
        for i in range(length):
            row = []
            for j in range(width):
                button = tk.Button(grid_frame, text="", width=4, height=2,
                                   command=lambda i=i, j=j: on_button_click(i, j))
                button.grid(row=i, column=j, padx=1, pady=1)
                row.append(button)
            buttons.append(row)
        grid_frame.buttons = buttons
        grid_frame.first_button_colored = False
        grid_frame.press_count = 0
        grid_frame.total_buttons = length * width
        grid_frame.press_history = []  # List to store the history of button presses
        grid_frame.current_index = -1  # Index to keep track of current position in the history

        # Lock the size of the columns and rows
        for i in range(length):
            grid_frame.grid_rowconfigure(i, minsize=10)
        for j in range(width):
            grid_frame.grid_columnconfigure(j, minsize=20)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for length and width")


def on_button_click(i, j):
    button = grid_frame.buttons[i][j]
    if button.cget('bg') == 'red':
        return  # Return if the button is already colored red

    if not grid_frame.first_button_colored:
        # Color the first button red and number it
        button.configure(bg='red', text=str(grid_frame.press_count + 1))
        grid_frame.press_history.append((i, j))
        grid_frame.current_index += 1
        grid_frame.press_count += 1
        grid_frame.first_button_colored = True
    else:
        # Only color this button red if it has exactly 1 or 3 adjacent red buttons
        adjacent_count = count_adjacent_red(i, j)
        if adjacent_count == 1 or adjacent_count == 3:
            button.configure(bg='red', text=str(grid_frame.press_count + 1))
            grid_frame.press_history = grid_frame.press_history[
                                       :grid_frame.current_index + 1]  # Truncate history beyond current index
            grid_frame.press_history.append((i, j))
            grid_frame.current_index += 1
            grid_frame.press_count += 1

    # Check for end conditions
    check_end_conditions()


def count_adjacent_red(i, j):
    count = 0
    if i > 0 and grid_frame.buttons[i - 1][j].cget('bg') == 'red':
        count += 1
    if i < len(grid_frame.buttons) - 1 and grid_frame.buttons[i + 1][j].cget('bg') == 'red':
        count += 1
    if j > 0 and grid_frame.buttons[i][j - 1].cget('bg') == 'red':
        count += 1
    if j < len(grid_frame.buttons[0]) - 1 and grid_frame.buttons[i][j + 1].cget('bg') == 'red':
        count += 1
    return count


def check_end_conditions():
    if grid_frame.press_count == grid_frame.total_buttons:
        messagebox.showinfo("Game Over", "All buttons are pressed!")
        return

    for i in range(len(grid_frame.buttons)):
        for j in range(len(grid_frame.buttons[0])):
            if grid_frame.buttons[i][j].cget('bg') != 'red':
                adjacent_count = count_adjacent_red(i, j)
                if adjacent_count == 1 or adjacent_count == 3:
                    return
    messagebox.showinfo("Game Over", "No more buttons can be pressed!")


def reset_to_input():
    # Clear the grid
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Show input widgets
    length_label.grid(row=0, column=0, padx=10, pady=10)
    length_entry.grid(row=0, column=1, padx=10, pady=10)
    width_label.grid(row=1, column=0, padx=10, pady=10)
    width_entry.grid(row=1, column=1, padx=10, pady=10)
    generate_button.grid(row=2, column=0, columnspan=2, pady=10)


def clear_all_coloring():
    for i in range(len(grid_frame.buttons)):
        for j in range(len(grid_frame.buttons[0])):
            grid_frame.buttons[i][j].configure(bg='white', text="")
    grid_frame.first_button_colored = False
    grid_frame.press_count = 0
    grid_frame.press_history = []
    grid_frame.current_index = -1


def navigate_history(direction):
    if direction == 'back':
        if grid_frame.current_index > 0:
            i, j = grid_frame.press_history[grid_frame.current_index]
            grid_frame.buttons[i][j].configure(bg='white', text="")
            grid_frame.current_index -= 1
    elif direction == 'forward':
        if grid_frame.current_index < len(grid_frame.press_history) - 1:
            grid_frame.current_index += 1
            i, j = grid_frame.press_history[grid_frame.current_index]
            grid_frame.buttons[i][j].configure(bg='red', text=str(grid_frame.press_history.index((i, j)) + 1))


# Create the main window
root = tk.Tk()
root.title("Button Grid Generator")

# Bind the 'r' key to reset the interface
root.bind('<r>', lambda event: reset_to_input())

# Bind the 'e' key to clear all coloring
root.bind('<e>', lambda event: clear_all_coloring())

# Bind the arrow keys to navigate the history
root.bind('<Left>', lambda event: navigate_history('back'))
root.bind('<Right>', lambda event: navigate_history('forward'))

# Create and place the length and width entry fields and labels
length_label = tk.Label(root, text="Length:")
length_label.grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

width_label = tk.Label(root, text="Width:")
width_label.grid(row=1, column=0, padx=10, pady=10)
width_entry = tk.Entry(root)
width_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the generate button
generate_button = tk.Button(root, text="Generate Grid", command=generate_grid)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a frame to hold the grid of buttons
grid_frame = tk.Frame(root)
grid_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
grid_frame.buttons = []

# Run the main loop
root.mainloop()
