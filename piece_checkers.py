import math


def check_pawn(board, color, from_, to):
    """
    Checks if a given move is possible for a pawn, there are 4 cases for this.
    Move one forward: when spot in front is free.
    Move two forward: when both spots in front are free, and only on first turn (y is 1 for black, or 6 for white).
    Move one diagonally forward: when a piece is diagonally in front of it.
    Move one diagonally forward: When the piece directly to that side is a pawn that has just moved two forward.
    """

    # Case 1 and 2
    if from_[0] == to[0]:
        direction = 1 if color == "b" else -1
        first_turn = from_[1] == ((8 + direction) % 8)
        if (from_[1] + direction == to[1]) and (board.get(*to) == ""):
            return True
        elif first_turn and (from_[1] + direction * 2 == to[1]) and (board.get(to[0], to[1] + direction) == "") and (board.get(*to) == ""):
            return True
        else:
            return False
    else:
        return False  # TODO: Rest of pawn movement
