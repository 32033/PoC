import tkinter as tk
from typing import Union
from board import Board
from piece_checkers import *

window = tk.Tk()
board = Board()

currently_selected: Union[tuple[int, int], None] = None

def square_clicked(destination):
    """
    Called when a button on the board is clicked.
    If no piece is selected, then the clicked piece is selected.

    If a selected piece is clicked, then it is unselected.
    If an unselected piece is clicked, then the piece moves there.

    This assumes only buttons with valid moves can be clicked.

    The board will be redrawn after any changes have been made.
    """
    global currently_selected

    if currently_selected is None:  # Check nothing selected
        currently_selected = destination

    elif destination == currently_selected:  # Check unselect
        currently_selected = None

    else:  # Move piece
        piece = board.get(*currently_selected)
        board.set(*currently_selected, "")
        board.set(*destination, piece)
        currently_selected = None


    redraw_board()




def redraw_board():
    """
    Redraws the board by clearing it, then adding the new buttons and setting their attributes and states.
    """

    for widget in window.winfo_children():
        widget.destroy()

    for x in range(board.size):
        for y in range(board.size):
            piece = board.get(x, y)

            enabled: bool
            if currently_selected is None:
                enabled = piece != ""
            else:
                enabled = check_if_possible_move((x, y))

            piece = piece if piece != "" else "."

            b = tk.Button(window, text=piece, state=tk.DISABLED if not enabled else tk.NORMAL,
                          command=lambda destination=(x, y): square_clicked(destination))
            b.grid(row=y, column=x)


def check_if_possible_move(destination):
    """
    Checks if it is possible to move the piece at currently_selected to the coords at coords.
    Returns true if the move is possible.
    Returns true if the move is the same.
    """

    piece_color, piece_type = board.get(*currently_selected)
    if destination == currently_selected:  # Same piece return true
        return True
    elif piece_type == "p" and check_pawn(board, piece_color, currently_selected, destination):
        return True
    elif piece_type == "c" and check_castle(board, piece_color, currently_selected, destination):
        return True
    elif piece_type == "h" and check_horse(board, piece_color, currently_selected, destination):
        return True
    else:
        return False


redraw_board()
window.mainloop()