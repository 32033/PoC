import copy
import tkinter as tk
from typing import Union
from board import Board
from piece_checkers import *

window = tk.Tk()
board = Board()

debug_colors: bool = True  # Show colors depending on the states of various parts of the board

currently_selected: Union[tuple[int, int], None] = None

turn: int = 0  # Even or 0 for white, odd for black

def square_clicked(destination):
    """
    Called when a button on the board is clicked.
    If no piece is selected, then the clicked piece is selected.

    If a selected piece is clicked, then it is unselected.
    If an unselected piece is clicked, then the piece moves there.

    This assumes only buttons with valid moves can be clicked.

    The board will be redrawn after any changes have been made.
    """
    global currently_selected, turn

    no_redraw = False  # Should we not redraw the board afterward

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

        # Check pawn promotion
        if piece[1] == "p" and destination[1] % 7 == 0:
            # ^ Checks if it is a pawn, and it is on the top or bottom row
            promote(destination)  # Changes ui, so do not redraw afterwards
            no_redraw = True

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
        turn += 1

    if not no_redraw:
        redraw_board()




def redraw_board():
    """
    Redraws the board by clearing it, then adding the new buttons and setting their attributes and states.
    """

    for widget in window.winfo_children():
        widget.destroy()

    found_possible_move: bool = False

    for x in range(board.size):
        for y in range(board.size):
            piece = board.get(x, y)

            enabled: bool
            if currently_selected is None:
                enabled = (piece != "" and 
                           ((turn % 2 == 0 and (piece != "" and piece[0] == "w")) or  # White turn and piece is white
                            (turn % 2 == 1 and (piece != "" and piece[0] == "b"))))  # Black turn and piece is black
                enabled = enabled and has_possible_moves((x, y))  # Check if piece has possible moves that do not put us in check
                found_possible_move = enabled or found_possible_move
            else:
                enabled = check_if_possible_move(currently_selected, (x, y), board)  # Manages teams for us, and checks that moves do not allow check

            piece = piece if piece != "" else "."

            color = None
            if debug_colors:
                if board.is_en_passant(x, y):
                    color = "red"

            b = tk.Button(window, fg=color, text=piece, state=tk.DISABLED if not enabled else tk.NORMAL,
                          command=lambda destination=(x, y): square_clicked(destination))
            b.grid(row=y, column=x)

    # Check for checkmates / stalemates
    if currently_selected is None and not found_possible_move:
        if check_checked("w", board) and turn % 2 == 0:  # White to move, but nothing to get out of check and in check
            tk.Label(window, text="Black wins").grid(columnspan=8)
        elif check_checked("b", board) and turn % 2 == 1:  # Black to move, but nothing to get out of check and in check
            tk.Label(window, text="White wins").grid(columnspan=8)
        else:  # Not in check but no moves
            tk.Label(window, text="Stalemate").grid(columnspan=8)


def check_if_possible_move(from_: tuple[int, int], to: tuple[int, int], test_board: Board):
    """
    Checks if it is possible to move the piece at currently_selected to the coords at coords.
    Returns true if the move is possible.
    Returns true if the move is the same.
    :param test_board: The board to use
    """

    # Check move is valid
    piece_color, piece_type = test_board.get(*from_)
    if to == from_:  # Same piece return true
        return True
    elif piece_type == "p" and check_pawn(test_board, piece_color, from_, to):
        pass
    elif piece_type == "c" and check_castle(test_board, piece_color, from_, to):
        pass
    elif piece_type == "h" and check_horse(test_board, piece_color, from_, to):
        pass
    elif piece_type == "b" and check_bishop(test_board, piece_color, from_, to):
        pass
    elif piece_type == "q" and check_queen(test_board, piece_color, from_, to):
        pass
    elif piece_type == "k" and check_king(test_board, piece_color, from_, to):
        pass
    else:
        return False  # Cannot move piece there so return false

    # Moves are valid, but now we need to test if the cause check
    new_test_board = copy.deepcopy(test_board)
    new_test_board.set(*to, test_board.get(*from_))
    new_test_board.set(*from_, "")
    try:
        return not check_checked(piece_color, new_test_board)  # If doesn't cause check then return True
    except NoKingException:
        return False  # As probably resulted in a check


class NoKingException(Exception):
    def __init__(self, color: str):
        self.color = color

    def __str__(self):
        return f"No king with color \"{self.color}\" found!"


def check_checked(color: str, test_board: Board) -> bool:
    """
    An internal helper function to check if the king of a certain color would be in check.
    This can check a duplicate of the board so unmade moves can be checked.
    :param color: The color of the king
    :param test_board: The board to use
    :return: True if in check
    """

    color2: str  # Color of piece attacking the king
    if color == "b":
        color2 = "w"
    else:
        color2 = "b"

    # First we locate which square the king is at
    for x in range(test_board.size):
        for y in range(test_board.size):
            if test_board.get(x, y) == color + "k":
                break
        else:  # If y is not broke then enter this block
            continue
        break  # First loop broke, so break outer
    else: # Outer was not broke so king not found
        raise NoKingException(color)

    # King is at (x, y). Now check if any piece of color2 can take it
    for x2 in range(test_board.size):
        for y2 in range(test_board.size):
            piece = test_board.get(x2, y2)

            if piece == "":
                continue
            elif piece[0] == color2:

                if check_if_possible_move((x2, y2), (x, y), test_board):
                    return True
    return False


def has_possible_moves(from_: tuple[int, int]):
    """
    Checks if there are any possible moves from the given location that do not result in the king of the same color being in check afterwards.
    :return: True if there are possible moves
    """

    possible_move = False

    # To do this we loop through every possible move this piece has
    for x in range(board.size):
        for y in range(board.size):
            if (x, y) == from_:  # We don't care about this
                continue

            if check_if_possible_move(from_, (x, y), board):  # Will check if move puts us in check
                possible_move = True

    return possible_move


def promote(loc: tuple[int, int]):
    """
    Handles the promotion of a pawn, this takes a location of a piece. Then gives the user buttons to select what to
    promote it to. The color is taken from the piece that used to be at that board location.
    """
    def do_promotion(x, y, name: str):
        color = board.get(x, y)[0]
        board.set(x, y, color + name)
        redraw_board()  # Will reset the buttons

    for widget in window.winfo_children():
        widget.destroy()

    tk.Button(window, text="castle", command=lambda loc_=loc: do_promotion(*loc_, "c")).pack()
    tk.Button(window, text="horse", command=lambda loc_=loc: do_promotion(*loc_, "h")).pack()
    tk.Button(window, text="priest", command=lambda loc_=loc: do_promotion(*loc_, "b")).pack()
    tk.Button(window, text="queen", command=lambda loc_=loc: do_promotion(*loc_, "q")).pack()



redraw_board()
window.mainloop()