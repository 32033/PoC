from math import *


def check_pawn(board, color, from_, to):
    """
    Checks if a given move is possible for a pawn, there are 4 cases for this.
    Move one forward: when spot in front is free.
    Move two forward: when both spots in front are free, and only on first turn (y is 1 for black, or 6 for white).
    Move one diagonally forward: when a piece is diagonally in front of it.
    Move one diagonally forward: When the piece directly to that side is a pawn that has just moved two forward.
    """

    direction = 1 if color == "b" else -1

    # Case 1 and 2
    if from_[0] == to[0]:
        first_turn = (color == "b" and from_[1] == 1) or (color == "w" and from_[1] == 6)

        if (from_[1] + direction == to[1]) and (board.get(*to) == ""):
            return True
        elif first_turn and (from_[1] + direction * 2 == to[1]) and (board.get(to[0], to[1] - direction) == "") and (board.get(*to) == ""):
            return True
        else:
            return False
    
    # Case 2
    elif abs(from_[0] - to[0]) == 1 and from_[1] + direction == to[1]:  # Checks if on adjacant column and 1 movement forward
        if board.get(*to) != "" and board.get(*to)[0] != color:  # If space is not free and color is opposite
            return True
        else:
            return False
    else:
        return False  # TODO: Case 3

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
    Can only move on diagonalls in a straigt line. All the spaces in between must be free.
    """

    horizontal = abs(from_[0] - to[0])
    vertical = abs(from_[1] - to[1])

    if horizontal == vertical:  # Check moving diagonally

        # Check spaces are free
        x_multiplier = -(from_[0] - to[0]) / horizontal
        y_multiplier = -(from_[1] - to[1]) / vertical
        for n in range(1, horizontal + 1):
            x = int(from_[0] + n * x_multiplier)
            y = int(from_[1] + n * y_multiplier)
            print(x, y, from_, n)
            if board.get(x, y) != "":
                return False
            # TODO: collide with other pieces
        return True
    
    else:
        return False