import tkinter as tk
from typing import Union
from board import Board
from piece_checkers import *

window = tk.Tk()
board = Board()

currently_selected: Union[tuple[int, int], None] = [1, 1]


def update_buttons():
    for widget in window.winfo_children():
        widget.destroy()

    for x in range(board.size):
        for y in range(board.size):
            piece_type = board.get(x, y)

            enabled: bool
            if currently_selected is None:
                enabled = piece_type != ""
            else:
                enabled = check_if_possible_move([x, y])

            piece_type = piece_type if piece_type != "" else "."

            b = tk.Button(window, text=piece_type, state=tk.DISABLED if not enabled else tk.NORMAL)
            b.grid(row=y, column=x)

"""
    Checks if it is possible to move the piece at currently_selected to the coords at coords.
    Returns true if the move is possible.
    Returns true if the move is the same.
"""
def check_if_possible_move(destination):
    piece_color, piece_type = board.get(*currently_selected)

    if destination == currently_selected:  # Same piece return true
        return True
    elif piece_type == "p" and check_pawn(board, piece_color, currently_selected, destination):
        return True
    else:
        return False


update_buttons()
window.mainloop()