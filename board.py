class Board:
    size: int = 8
    pieces: list[str]

    def __init__(self):
        self.pieces = Board.make_new()

    def get(self, x, y):
        return self.pieces[x + y * Board.size]
     
    @staticmethod
    def make_new():
        board = []

        # Add blacks
        board.append("bc")
        board.append("bh")
        board.append("bb")
        board.append("bq")
        board.append("bk")
        board.append("bb")
        board.append("bh")
        board.append("bc")
        for i in range(Board.size): board.append("bp")

        # Empty space
        for i in range(Board.size * (Board.size - 4)): board.append("")  # Empty space of width * height - (2 for pawns, and 2 for special pieces)

        # Add whites
        for i in range(Board.size): board.append("wp")
        board.append("wc")
        board.append("wh")
        board.append("wb")
        board.append("wq")
        board.append("wk")
        board.append("wb")
        board.append("wh")
        board.append("wc")

        return board
