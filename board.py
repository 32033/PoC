from typing import Union


class Board:
    size: int = 8
    pieces: list[str]
    en_passant: Union[tuple[int, int], None]
    moved: set[int]

    def __init__(self):
        self.pieces = Board.make_new()
        self.en_passant_able = set()
        self.en_passant = None
        self.moved = set()

    def get(self, x, y):
        return self.pieces[x + y * Board.size]

    def set(self, x, y, piece):
        self.pieces[x + y * Board.size] = piece
        self.moved.add(x + y * Board.size)

    def has_moved(self, x, y):
        return (x + y * Board.size) in self.moved

    def set_en_passant(self, x, y):
        """
        Declare the piece at this location as able to be en passant ed.
        """
        self.en_passant = (x, y)

    def is_en_passant(self, x, y):
        """
        Returns true if the piece at this location is eligible to be en passant ed.
        """
        return (x, y) == self.en_passant

    def remove_en_passant(self):
        """
        Invalidates the current en passant.
        """
        self.en_passant = None

    @staticmethod
    def make_new():
        board = []

        # Add blacks
        board += ["bc", "bh", "bb", "bq", "bk", "bb", "bh", "bc"]
        board += ["bp"] * 8
        #board += [""] * 8

        # Empty space
        board += [""] * (Board.size * (Board.size - 4))  # Empty space of width * height - (2 for pawns, and 2 for special pieces)

        # Add whites
        #board += [""] * 8
        board += ["wp"] * 8
        board += ["wc", "wh", "wb", "wq", "wk", "wb", "wh", "wc"]

        return board
