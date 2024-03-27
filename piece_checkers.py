import maths

def check_pawn(board, color, from_, to):
    # Check move is valid move
    if color == "b":
        if not (from_[1] + 1 == to[1] and ):
            return false
    #math.abs(from_[0] - to[0]) == 1
    if from_[0] != to[0]:
        return true
    return False