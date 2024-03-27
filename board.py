class Board:
    size: int = 8
    pieces: list[str]

    def __init__(self):
        self.pieces = Board.make_new()

    def get(self, x, y):
        return self.pieces[x + y * Board.size]

    def set(self, x, y, piece):
        self.pieces[x + y * Board.size] = piece


    @staticmethod
    def make_new():
        board = []

        # Add blacks
        board += ["bc", "bh", "bb", "bq", "bk", "bb", "bh", "bc"]
        for i in range(Board.size): board.append("bp")

        # Empty space
        for i in range(Board.size * (Board.size - 4)): board.append("")  # Empty space of width * height - (2 for pawns, and 2 for special pieces)

        # Add whites
        for i in range(Board.size): board.append("wp") 
        board += ["wc", "wh", "wb", "wq", "wk", "wb", "wh", "wc"]

        return board
