import tkinter as tk
from typing import Union
from board import Board
from piece_checkers import *

window = tk.Tk()
board = Board()

currently_selected: Union[tuple[int, int], None] = [1, 0]


def update_buttons():
    for widget in window.winfo_children():
        widget.destroy()

    for x in range(board.size):
        for y in range(board.size):
            piece_type = board.get(x, y)

            disabled = (piece_type == "") or ((currently_selected != None) and (not check_if_possible_move([x, y])))

            b = tk.Button(window, text=piece_type, state=tk.DISABLED if disabled else tk.NORMAL)
            b.grid(row=y, column=x)

"""
    Checks if it is possible to move the piece at currently_selected to the coords at coords.
    Returns true if they are the same coords.
"""
def check_if_possible_move(coords):
    piece_color, piece_type = board.get(*coords)

    if coords == currently_selected:  # Same piece return true
        return True
    elif check_pawn(board, piece_color, currently_selected, coords):
        pass
    else:
        return False


update_buttons()
window.mainloop()