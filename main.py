import tkinter as tk
from typing import Union
from board import Board
from piece_checkers import *

# TODO: Checking if in check
# TODO:     And hence checking if in check mate
# TODO: Pawn promotion
# TODO: Turns?

window = tk.Tk()
board = Board()

debug_colors: bool = True  # Show colors depending on the states of various parts of the board

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

        # Check kill via en passant
        if piece[1] == "p" and currently_selected[0] != destination[0] and board.get(*destination) != "":
            # ^ If the piece being moved is a pawn, it moves in the x direction but to an empty space
            board.set(destination[0], currently_selected[1], "")

        # Check enable en passant
        if piece[1] == "p" and currently_selected[0] == destination[0] and abs(currently_selected[1] - destination[1]) == 2:
            # ^ Checks if it is a pawn, the x is the same, and the y changed by two
            board.set_en_passant(*destination)
        else:  # Otherwise remove it
            board.remove_en_passant()

        # Check castling
        if piece[1] == "k" and not king_move_one(currently_selected, destination):  # If is king and moved more than one then it castled
            color = piece[0]
            if destination[0] < currently_selected[0]:  # Left castle
                board.set(*destination, color + "k")
                board.set(0, destination[1], "")
                board.set(3, destination[1], color + "c")
            else:  # Right castle
                board.set(*destination, color + "k")
                board.set(7, destination[1], "")
                board.set(5, destination[1], color + "c")

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

            color = None
            if debug_colors:
                if board.is_en_passant(x, y):
                    color = "red"

            b = tk.Button(window, fg=color, text=piece, state=tk.DISABLED if not enabled else tk.NORMAL,
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
    elif piece_type == "b" and check_bishop(board, piece_color, currently_selected, destination):
        return True
    elif piece_type == "q" and check_queen(board, piece_color, currently_selected, destination):
        return True
    elif piece_type == "k" and check_king(board, piece_color, currently_selected, destination):
        return True
    else:
        return False


redraw_board()
window.mainloop()