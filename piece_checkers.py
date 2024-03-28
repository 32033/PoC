from math import *


def check_pawn(board, color, from_, to):
    """
    Checks if a given move is possible for a pawn, there are 4 cases for this.
    Move one forward: when spot in front is free.
    Move two forward: when both spots in front are free, and only on first turn (y is 1 for black, or 6 for white).
    Move one diagonally forward: when a piece is diagonally in front of it.
    Move one diagonally forward: When the piece directly to that side is a pawn that has just moved two forward (en passant).
    """

    direction = 1 if color == "b" else -1

    # Case 1 and 2
    if from_[0] == to[0]:
        first_turn = (color == "b" and from_[1] == 1) or (color == "w" and from_[1] == 6)
        # Case 1
        if (from_[1] + direction == to[1]) and (board.get(*to) == ""):
            return True
        # Case 2
        elif first_turn and (from_[1] + direction * 2 == to[1]) and (board.get(to[0], to[1] - direction) == "") and (board.get(*to) == ""):
            return True
    
    # Case 3 and 4
    elif abs(from_[0] - to[0]) == 1 and from_[1] + direction == to[1]:  # Checks if on adjacent column and 1 movement forward
        # Case 3
        if board.get(*to) != "" and board.get(*to)[0] != color:  # If space is not free and color is opposite
            return True
        # Case 4
        elif board.get(*to) == "" and board.is_en_passant(to[0], from_[1]):  # If space is free and space on that side is en passant able
            return True

    else:
        return False

def check_castle(board, color, from_, to):
    """
    Can only move to places with the same x or y value, where all the spaces in between them are free.
    """

    piece_at_to = board.get(*to)
    if piece_at_to != "" and piece_at_to[0] == color:
        return False

    if from_[0] == to[0]:  # On same vertical line
        start = min(from_[1], to[1]) + 1
        end = max(from_[1], to[1]) - 1
        for y in range(start, end + 1):
            if board.get(from_[0], y) != "":
                return False
        return True
    elif from_[1] == to[1]:  # On same horizontal line
        start = min(from_[0], to[0]) + 1
        end = max(from_[0], to[0]) - 1
        for x in range(start, end + 1):
            if board.get(x, from_[1]) != "":
                return False
        return True
    else:  # Somewhere else
        return False
    
def check_horse(board, color, from_, to):
    """
    Can only move two in one direction and then one in the other direction.
    E.g. two up and one left.
    """

    horizontal = abs(from_[0] - to[0])
    vertical = abs(from_[1] - to[1])

    long = max(horizontal, vertical)
    short = min(horizontal, vertical)

    if long == 2 and short == 1:
        piece_at_to = board.get(*to)
        if piece_at_to == "" or piece_at_to[0] != color:
            return True
    return False

def check_bishop(board, color, from_, to):
    """
    Can only move on diagonals in a straight line. All the spaces in between must be free.
    """

    # Remove any pieces of same color as can't take own pieces.
    piece_at_to = board.get(*to)
    if piece_at_to != "" and piece_at_to[0] == color:
        return False

    horizontal = abs(from_[0] - to[0])
    vertical = abs(from_[1] - to[1])

    if horizontal == vertical:  # Check moving diagonally

        # Check spaces are free
        x_multiplier = -(from_[0] - to[0]) / horizontal
        y_multiplier = -(from_[1] - to[1]) / vertical
        for n in range(1, horizontal - 1):
            x = int(from_[0] + n * x_multiplier)
            y = int(from_[1] + n * y_multiplier)
            if board.get(x, y) != "":
                return False

        return True
    
    else:
        return False


def check_queen(*args):
    """
    Can move in the union of the movements of bishops and castles (AKA straights and diagonals)
    """
    return check_castle(*args) or check_bishop(*args)

def check_king(board, color, from_, to):
    """
    King can move one space in any direction, however cannot move into check.
    King can also castle given it hasn't moved, with a castle that also hasn't moved.
    """

    # Check wouldn't take own color
    piece_at_to = board.get(*to)
    if piece_at_to != "" and piece_at_to[0] == color:
        return False

    # TODO: Check if move will put in check
    if king_move_one(from_, to): # If moved straight, or moved one diagonally
        return True

    # Check castling
    if (to[0] == 6 and not board.has_moved(*from_) and not board.has_moved(7, from_[1]) and board.get(5, from_[1]) == ""
            and board.get(6, from_[1]) == ""):  # King moving also accounts for king position
        return True

    if (to[0] == 2 and not board.has_moved(*from_) and not board.has_moved(0, from_[1]) and board.get(1, from_[1]) == ""
            and board.get(2, from_[1]) == "" and board.get(3, from_[1]) == ""):
        return True

    return False

def king_move_one(from_, to):
    horizontal = abs(from_[0] - to[0])
    vertical = abs(from_[1] - to[1])
    sum_ = horizontal + vertical
    if sum_ == 1 or (sum_ == 2 and horizontal == vertical): # If moved straight, or moved one diagonally
        return True
    return False