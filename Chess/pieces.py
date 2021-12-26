from enum import IntEnum
from numpy import array
import json
import os
import pygame


class Color(IntEnum):
    BLACK = 1
    WHITE = 0


main_dir = os.path.split(os.path.abspath(__file__))[0]


def getImage(image, color):
    color = "l" if color == Color.WHITE else "d"
    string = "Chess_" + image + color + "t60.png"
    file = os.path.join(main_dir, "images", string)
    return pygame.image.load(file).convert_alpha()


class Piece:

    def __init__(self, color, image):
        self.color = color
        self.hasMoved = False
        self.image = getImage(image, color)
        self._attackingSquares = set()

    def getAttackingSquares(self):
        return self._attackingSquares

    def getMovableSquares(self, board, x, y):
        return {(x_, y_) for (x_, y_) in self._attackingSquares.copy() if board.canMoveTo(x, y, x_, y_)}

    def calcStraightMoves(self, board, pos, directions, maxLength):
        for direction in directions:
            for i in range(1, maxLength + 1):
                newX, newY = pos + direction * i
                if not board.isInbounds((newX, newY)): break
                self._attackingSquares.add((newX, newY))
                if board.getPieceAt(newX, newY) is not None: break

    def calcOrthogonalMoves(self, board, pos, maxLength):
        return self.calcStraightMoves(board, pos, array([[1, 0], [0, 1], [-1, 0], [0, -1]]), maxLength)

    def calcDiagonalMoves(self, board, pos, maxLength):
        return self.calcStraightMoves(board, pos, array([[1, 1], [-1, 1], [1, -1], [-1, -1]]), maxLength)

    def isKing(self):
        return False

    def notation(self, xy):
        x, y = xy
        return f"{'ABCDEFGH'[x]}{y + 1}"


class Pawn(Piece):

    def calcMoves(self, board, x, y):
        self._attackingSquares = {(x + 1, y + 1), (x - 1, y + 1)} if self.color == Color.BLACK \
            else {(x + 1, y - 1), (x - 1, y - 1)}
        self._attackingSquares = {pos for pos in self._attackingSquares if board.isInbounds(pos)}

    def getMovableSquares(self, board, x, y):
        captureMoves = {pos for pos in self._attackingSquares if board.canMoveTo(x, y, *pos) and
                        (piece := board.getPieceAt(*pos)) is not None and piece.color != self.color}
        d = 1 if self.color == Color.BLACK else -1
        if board.getPieceAt(x, y + 1 * d) is None and board.canMoveTo(x, y, x, y + 1 * d):
            captureMoves.add((x, y + 1 * d))
            if board.getPieceAt(x, y + 2 * d) is None and not self.hasMoved and board.canMoveTo(x, y, x, y + 2 * d):
                captureMoves.add((x, y + 2 * d))
        return captureMoves


class Bishop(Piece):

    def calcMoves(self, board, x, y):
        self._attackingSquares.clear()
        self.calcDiagonalMoves(board, array([x, y]), 7)


class Queen(Piece):

    def calcMoves(self, board, x, y):
        self._attackingSquares.clear()
        self.calcDiagonalMoves(board, array([x, y]), 7)
        self.calcOrthogonalMoves(board, array([x, y]), 7)


class Rook(Piece):

    def calcMoves(self, board, x, y):
        self._attackingSquares.clear()
        self.calcOrthogonalMoves(board, array([x, y]), 7)


class Knight(Piece):

    def calcMoves(self, board, x, y):
        self._attackingSquares = \
         {pos for x_, y_ in [(2, 1), (1, 2), (-2, 1), (1, -2), (-2, -1), (-1, -2), (2, -1), (-1, 2)]
          if board.isInbounds(pos := (x + x_, y + y_))}


class King(Piece):

    def calcMoves(self, board, x, y):
        self._attackingSquares.clear()
        self.calcDiagonalMoves(board, array([x, y]), 1)
        self.calcOrthogonalMoves(board, array([x, y]), 1)

    def isKing(self):
        return True


def _main():
    pass


if __name__ == "__main__":
    _main()
