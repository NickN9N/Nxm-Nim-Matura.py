import tkinter as tk
from itertools import product


# Funktion zum Erstellen der Spielmatrix
def create_empty_matrix(height, width):
    return [[0] * width for _ in range(height)]


# Funktion zur Darstellung der Matrizen mit tkinter
def display_matrices(matrices, height, width, group_mode=False, group=None, break_mode=False):
    canvas.delete("all")  # Lösche die vorherige Matrix
    x_offset = 20  # Abstand vom linken Canvasrand
    y_offset = 20  # Abstand vom oberen Canvasrand
    line_width = 1880  # Maximalbreite, bevor ein Zeilenumbruch erfolgt
    last_filled_count = 0  # Um die Anzahl gefärbter Quadrate zu verfolgen

    if group_mode and group is not None:
        # Wenn wir im Gruppenmodus sind, zeigen wir nur die Matrizen dieser Gruppe an
        for matrix in grouped_matrices[group]:
            current_filled_count = count_filled_squares(matrix)
            if break_mode and current_filled_count != last_filled_count:
                y_offset += height * 20 + 10  # Erhöhe y_offset für den Zeilenumbruch
                x_offset = 20  # Setze x_offset zurück für die nächste Zeile

            draw_matrix(matrix, x_offset, y_offset)
            last_filled_count = current_filled_count  # Update der letzten gefärbten Anzahl
            x_offset += width * 20 + 10  # Abstand zwischen Matrizen

            if x_offset > line_width:
                x_offset = 20  # Setze x_offset zurück für die nächste Zeile (20 Pixel Abstand)
                y_offset += height * 20 + 10  # Erhöhe y_offset für die nächste Zeile

    else:
        # Andernfalls zeigen wir alle Matrizen an
        for matrix in matrices:
            current_filled_count = count_filled_squares(matrix)
            if break_mode and current_filled_count != last_filled_count:
                y_offset += height * 20 + 10  # Erhöhe y_offset für den Zeilenumbruch
                x_offset = 20  # Setze x_offset zurück für die nächste Zeile

            draw_matrix(matrix, x_offset, y_offset)
            last_filled_count = current_filled_count  # Update der letzten gefärbten Anzahl
            x_offset += width * 20 + 10  # Abstand zwischen Matrizen

            if x_offset > line_width:
                x_offset = 20  # Setze x_offset zurück für die nächste Zeile (20 Pixel Abstand)
                y_offset += height * 20 + 10  # Erhöhe y_offset für die nächste Zeile


def draw_matrix(matrix, x_offset, y_offset):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            color = "black" if matrix[i][j] == 1 else "white"
            canvas.create_rectangle(
                x_offset + j * 20, y_offset + i * 20, x_offset + (j + 1) * 20, y_offset + (i + 1) * 20,
                fill=color, outline="black"
            )


def key_handler(event):
    global current_index, in_color_mode, current_group, in_break_mode

    if event.char == 'e':
        toggle_color_mode()
    elif event.char == 'p':
        toggle_break_mode()
    elif in_color_mode:
        handle_color_mode_navigation(event)
    else:
        handle_default_navigation(event)


def toggle_color_mode():
    global in_color_mode, current_group
    in_color_mode = not in_color_mode
    current_group = 0 if in_color_mode else current_index
    display_matrices(sorted_unique_matrices, height, width, group_mode=in_color_mode, group=current_group)


def toggle_break_mode():
    global in_break_mode
    in_break_mode = not in_break_mode
    display_matrices(sorted_unique_matrices, height, width, break_mode=in_break_mode)


def handle_color_mode_navigation(event):
    global current_group
    if event.keysym == "Right" and current_group < max_group:
        current_group += 1
        display_matrices(sorted_unique_matrices, height, width, group_mode=in_color_mode, group=current_group)
    elif event.keysym == "Left" and current_group > 0:
        current_group -= 1
        display_matrices(sorted_unique_matrices, height, width, group_mode=in_color_mode, group=current_group)


def handle_default_navigation(event):
    global current_index
    if event.keysym == "Right" and current_index < len(sorted_unique_matrices) - 1:
        current_index += 1
        display_matrices(sorted_unique_matrices, height, width)
    elif event.keysym == "Left" and current_index > 0:
        current_index -= 1
        display_matrices(sorted_unique_matrices, height, width)


def calculate_positions_without_symmetries(height, width):
    all_positions = set()  # Set, um sicherzustellen, dass keine Symmetrien gezählt werden
    valid_matrices = []  # Liste, um alle validen Matrizen zu speichern

    empty_matrix = create_empty_matrix(height, width)
    all_positions.add(tuple(map(tuple, empty_matrix)))
    valid_matrices.append(empty_matrix)

    for initial_x, initial_y in product(range(height), range(width)):
        matrix = create_empty_matrix(height, width)
        matrix[initial_x][initial_y] = 1

        all_positions.add(tuple(map(tuple, matrix)))
        valid_matrices.append(matrix)

        queue = [(matrix, [(initial_x, initial_y)])]  # Warteschlange für BFS

        while queue:
            current_matrix, visited = queue.pop(0)

            for x in range(height):
                for y in range(width):
                    if (x, y) not in visited and current_matrix[x][y] == 0:
                        filled_neighbors = count_filled_neighbors(current_matrix, x, y)

                        if filled_neighbors in [1, 3]:
                            new_matrix = [row[:] for row in current_matrix]
                            new_matrix[x][y] = 1
                            matrix_tuple = tuple(map(tuple, new_matrix))

                            if matrix_tuple not in all_positions:
                                all_positions.add(matrix_tuple)
                                valid_matrices.append(new_matrix)
                                queue.append((new_matrix, visited + [(x, y)]))

    distinct_positions_count = len(all_positions)
    return valid_matrices, distinct_positions_count


def count_filled_neighbors(matrix, x, y):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return sum(1 for dx, dy in neighbors if
               0 <= x + dx < len(matrix) and 0 <= y + dy < len(matrix[0]) and matrix[x + dx][y + dy] == 1)


def count_filled_squares(matrix):
    return sum(row.count(1) for row in matrix)


def generate_symmetries(matrix):
    symmetries = set()
    height = len(matrix)
    width = len(matrix[0])

    def add_symmetries(mat):
        symmetries.add(tuple(map(tuple, mat)))

    add_symmetries(matrix)
    add_symmetries([row[::-1] for row in matrix])
    add_symmetries(matrix[::-1])
    add_symmetries([row[::-1] for row in matrix[::-1]])
    add_symmetries(list(zip(*matrix[::-1])))
    add_symmetries(list(zip(*matrix))[::-1])

    return symmetries


def categorize_matrices(matrices):
    unique_matrices = []
    seen_symmetries = set()

    for matrix in matrices:
        symmetries = generate_symmetries(matrix)
        if not seen_symmetries.intersection(symmetries):
            unique_matrices.append(matrix)
            seen_symmetries.update(symmetries)

    return unique_matrices


if __name__ == "__main__":
    height = int(input("Geben Sie die Höhe der Matrix ein: "))
    width = int(input("Geben Sie die Breite der Matrix ein: "))

    valid_matrices, distinct_positions_count = calculate_positions_without_symmetries(height, width)
    unique_matrices = categorize_matrices(valid_matrices)
    unique_positions_count = len(unique_matrices)

    print(f"Die totale Anzahl an verschiedenen Positionen (ohne Symmetrien) ist: {distinct_positions_count}")
    print(
        f"Die totale Anzahl an verschiedenen Positionen (eine pro symmetrischer Gruppe) ist: {unique_positions_count}")

    sorted_unique_matrices = sorted(unique_matrices, key=count_filled_squares)
    grouped_matrices = {}

    for matrix in sorted_unique_matrices:
        count = count_filled_squares(matrix)
        if count not in grouped_matrices:
            grouped_matrices[count] = []
        grouped_matrices[count].append(matrix)

    # Finde die Matrix mit den meisten gefüllten Quadraten
    max_filled_squares = max(grouped_matrices.keys())
    print(f"Die maximale Anzahl gefüllter Quadrate in einer Matrix ist: {max_filled_squares}")

    root = tk.Tk()
    root.title("Spielpositionen")
    root.state('zoomed')
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()

    current_index = 0
    in_color_mode = False
    current_group = 0
    max_group = len(grouped_matrices) - 1
    in_break_mode = False

    root.bind("<Key>", key_handler)
    display_matrices(sorted_unique_matrices, height, width)
    root.mainloop()
