import tkinter as tk
from tkinter import messagebox
import numpy as np
import random


class NimGame:
    def __init__(self, master, feld_groessen, gegen_computer=False):
        self.master = master
        self.master.title("Nim-Spiel")
        self.player_turn = 1  # Start bei Spieler 1
        self.current_field = None  # Aktuelles Feld, in dem der Spieler arbeitet
        self.felder = []  # Liste für die Spielfelder (flexible Anzahl)
        self.feld_buttons = []  # Buttons für jedes Spielfeld
        self.gegen_computer = gegen_computer  # Ob gegen den Computer gespielt wird

        # Spielfelder initialisieren
        for feld_num, (breite, hoehe) in enumerate(feld_groessen):
            feld = np.zeros((hoehe, breite), dtype=int)
            self.felder.append(feld)

            # Erstellen des Feldes als Buttons
            buttons = []
            frame = tk.Frame(self.master)
            frame.grid(row=0, column=feld_num, padx=10)  # `grid` für die Layout-Positionierung
            label = tk.Label(frame, text=f"Feld {feld_num + 1}")
            label.grid(row=0, column=0, columnspan=breite)  # Spielfeldtitel

            for i in range(hoehe):
                row_buttons = []
                for j in range(breite):
                    button = tk.Button(frame, width=4, height=2, bg='white',
                                       command=lambda r=i, c=j, f=feld_num: self.select_square(r, c, f))
                    button.grid(row=i + 1, column=j)  # Beachte `row=i+1`, um Platz für das Label zu lassen
                    row_buttons.append(button)
                buttons.append(row_buttons)
            self.feld_buttons.append(buttons)

        # Button, um den Zug zu beenden und den Spieler zu wechseln
        self.end_turn_button = tk.Button(self.master, text="Zug beenden", command=self.end_turn)
        self.end_turn_button.grid(row=1, column=1, pady=20)

    def select_square(self, row, col, feld_num):
        """Färbt ein Quadrat im gewählten Feld ein, wenn der Zug gültig ist."""
        feld = self.felder[feld_num]

        # Wenn der Spieler noch kein Feld gewählt hat, wird das aktuelle Feld festgelegt
        if self.current_field is None:
            self.current_field = feld_num

        # Spieler darf nur im selben Feld mehrere Quadrate einfärben
        if feld_num != self.current_field:
            messagebox.showwarning("Ungültiger Zug", "Du kannst nur in einem Feld pro Zug Quadrate einfärben.")
            return

        # Prüfen, ob das Quadrat bereits eingefärbt ist
        if feld[row, col] == 1:
            messagebox.showwarning("Ungültiger Zug", "Dieses Quadrat ist bereits eingefärbt.")
            return

        # Beim ersten Zug in einem leeren Feld: beliebiges Quadrat
        if np.sum(feld) == 0:
            self.feld_buttons[feld_num][row][col].config(bg='blue' if self.player_turn == 1 else 'red')
            feld[row, col] = 1
        else:
            # Prüfen, ob das Quadrat gemäß den Nachbarschaftsregeln eingefärbt werden darf
            valid = self.is_valid_move(feld, row, col)
            if valid:
                self.feld_buttons[feld_num][row][col].config(bg='blue' if self.player_turn == 1 else 'red')
                feld[row, col] = 1
            else:
                messagebox.showwarning("Ungültiger Zug", "Dieses Quadrat kann nicht eingefärbt werden.")
                return

    def is_valid_move(self, feld, row, col):
        """Überprüft, ob ein Zug gültig ist, basierend auf den Nachbarschaftsregeln."""
        # Nachbarn (oben, unten, links, rechts)
        angrenzend = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        angrenzende_felder = sum(
            [feld[x, y] == 1 for x, y in angrenzend if 0 <= x < feld.shape[0] and 0 <= y < feld.shape[1]])
        return angrenzende_felder == 1 or angrenzende_felder == 3

    def end_turn(self):
        """Wechselt den Spieler und überprüft, ob das Spiel zu Ende ist."""
        # Prüfen, ob das Spiel zu Ende ist
        if self.check_game_over():
            messagebox.showinfo("Spielende", f"Spieler {self.player_turn} hat gewonnen!")
            self.master.quit()
            return

        # Spieler wechseln
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.current_field = None  # Beim nächsten Spieler kann ein neues Feld ausgewählt werden

        # Wenn der Gegner ein Computer ist und der Computer dran ist
        if self.gegen_computer and self.player_turn == 2:
            self.computer_move()
        else:
            messagebox.showinfo("Spielerwechsel", f"Jetzt ist Spieler {self.player_turn} dran!")

    def check_game_over(self):
        """Prüft, ob alle Quadrate eingefärbt sind."""
        for feld in self.felder:
            if np.any(feld == 0):  # Es gibt noch nicht eingefärbte Quadrate
                return False
        return True

    def computer_move(self):
        """Computerzug: Färbt zufällig ein Quadrat ein."""
        valid_move_found = False

        # Versuche, einen zufälligen gültigen Zug zu finden
        while not valid_move_found:
            feld_num = random.choice(
                [i for i in range(len(self.felder)) if np.any(self.felder[i] == 0)])  # Wähle ein nicht volles Feld
            feld = self.felder[feld_num]
            hoehe, breite = feld.shape

            # Wenn das Feld noch leer ist, wählt der Computer ein beliebiges Quadrat
            if np.sum(feld) == 0:
                row, col = random.randint(0, hoehe - 1), random.randint(0, breite - 1)
                self.select_square(row, col, feld_num)
                valid_move_found = True
            else:
                # Suche nach einem Quadrat, das gemäß den Regeln eingefärbt werden kann
                for _ in range(100):  # Maximal 100 Versuche, eine gültige Position zu finden
                    row, col = random.randint(0, hoehe - 1), random.randint(0, breite - 1)
                    if feld[row, col] == 0 and self.is_valid_move(feld, row, col):
                        self.select_square(row, col, feld_num)
                        valid_move_found = True
                        break

        # Zug beenden, nachdem der Computer gespielt hat
        self.end_turn()


def start_game():
    """Startet das Nim-Spiel mit benutzerdefinierten Größen für die Felder."""
    feld_anzahl = int(input("Wie viele Felder möchtest du spielen (z.B. 2, 3, 4)? "))

    feld_groessen = []
    for i in range(feld_anzahl):
        breite = int(input(f"Breite des Feldes {i + 1}: "))
        hoehe = int(input(f"Höhe des Feldes {i + 1}: "))
        feld_groessen.append((breite, hoehe))

    # Wahl: gegen Computer oder gegen anderen Spieler
    gegen_computer = input("Möchtest du gegen den Computer spielen? (ja/nein): ").lower() == 'ja'

    # Tkinter-Fenster initialisieren
    root = tk.Tk()
    game = NimGame(root, feld_groessen, gegen_computer)
    root.mainloop()


# Spiel starten
start_game()
