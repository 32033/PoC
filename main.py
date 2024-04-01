import tkinter as tk
from typing import Union
from board import Board
from piece_checkers import *

# TODO: ~~Checking if in check~~
# TODO:     And hence checking if in check mate
# TODO: Pawn promotion
# TODO: Turns?

window = tk.Tk()
board = Board()

debug_colors: bool = True  # Show colors depending on the states of various parts of the board

currently_selected: Union[tuple[int, int], None] = None

black_check: bool = False  # Is black currently in check
white_check: bool = False  # Is white currently in check

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

        update_checked()
        print(white_check, black_check)

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
                enabled = check_if_possible_move(currently_selected, (x, y))

            piece = piece if piece != "" else "."

            color = None
            if debug_colors:
                if board.is_en_passant(x, y):
                    color = "red"
                if black_check and piece == "bk":
                    color = "yellow"
                if white_check and piece == "wk":
                    color = "yellow"

            b = tk.Button(window, fg=color, text=piece, state=tk.DISABLED if not enabled else tk.NORMAL,
                          command=lambda destination=(x, y): square_clicked(destination))
            b.grid(row=y, column=x)


def check_if_possible_move(from_: tuple[int, int], to):
    """
    Checks if it is possible to move the piece at currently_selected to the coords at coords.
    Returns true if the move is possible.
    Returns true if the move is the same.
    """

    piece_color, piece_type = board.get(*from_)
    if to == from_:  # Same piece return true
        return True
    elif piece_type == "p" and check_pawn(board, piece_color, from_, to):
        return True
    elif piece_type == "c" and check_castle(board, piece_color, from_, to):
        return True
    elif piece_type == "h" and check_horse(board, piece_color, from_, to):
        return True
    elif piece_type == "b" and check_bishop(board, piece_color, from_, to):
        return True
    elif piece_type == "q" and check_queen(board, piece_color, from_, to):
        return True
    elif piece_type == "k" and check_king(board, piece_color, from_, to):
        return True
    else:
        return False

def update_checked():
    """
    Update the global flags: black_check and white_check.
    """
    global black_check, white_check

    def check_checked(color: str, color2: str) -> bool:
        """
        An internal helper function to check if the king of a certain color would be in check.
        :param color: The color of the king
        :param color2: The color of the pieces attacking the king
        :return: True if in check
        """

        # First we locate which square the king is at
        for x in range(board.size):
            for y in range(board.size):
                if board.get(x, y) == color + "k":
                    break
            else:  # If y is not broke then enter this block
                continue
            break  # First loop broke, so break outer
        else: # Outer was not broke so king not found
            raise Exception(f"No king with color \"{color}\" found!")

        # King is at (x, y). Now check if any piece of color2 can take it
        for x2 in range(board.size):
            for y2 in range(board.size):
                piece = board.get(x2, y2)

                if piece == "":
                    continue
                elif piece[0] == color2:
                    if check_if_possible_move((x2, y2), (x, y)):
                        return True
        return False

    black_check = check_checked("b", "w")
    white_check = check_checked("w", "b")


redraw_board()
window.mainloop()