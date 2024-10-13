from itertools import product

# Funktion zum Erstellen der Spielmatrix
def create_empty_matrix(height, width):
    return [[0] * width for _ in range(height)]

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
