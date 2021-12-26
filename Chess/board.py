import json

import pygame

import pieces
pygame.init()
pygame.display.set_mode()


class Board:

    PIECES = {"b": pieces.Bishop, "k": pieces.King, "q": pieces.Queen, "r": pieces.Rook, "n": pieces.Knight,
              "p": pieces.Pawn}

    def __init__(self):
        self.squares = [
             ["R", "N", "B", "Q", "K", "B", "N", "R"],
             ["P", "P", "P", "P", "P", "P", "P", "P"],
             ["E", "E", "E", "E", "E", "E", "E", "E"],
             ["E", "E", "E", "E", "E", "E", "E", "E"],
             ["E", "E", "E", "E", "E", "E", "E", "E"],
             ["E", "E", "E", "E", "E", "E", "E", "E"],
             ["p", "p", "p", "p", "p", "p", "p", "p"],
             ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]
        self.squares = [[self.PIECES[c](sq.isupper(), c) if (c := sq.lower()) in self.PIECES else None
                        for sq in row] for row in self.squares]
        self.updatePieceMoves()

    def getPieceAt(self, x, y):
        return self.squares[y][x]

    def isInbounds(self, pos):
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7

    def movePiece(self, x, y, x1, y1, isRealMove=True):
        temp = self.squares[y1][x1]
        self.squares[y1][x1] = self.squares[y][x]
        self.squares[y][x] = None
        self.updatePieceMoves()
        if isRealMove:
            self.squares[y1][x1].hasMoved = True
        return temp

    def updatePieceMoves(self):
        for y in range(8):
            for x in range(8):
                if self.squares[y][x] is not None:
                    self.squares[y][x].calcMoves(self, x, y)

    def isKingAttacked(self, color):
        attackedSquares = set()
        kingPos = (-1, -1)
        for y in range(8):
            for x in range(8):
                if (piece := self.squares[y][x]) is not None:
                    if piece.color == color:
                        if piece.isKing():
                            kingPos = x, y
                    else:
                        attackedSquares = attackedSquares.union(piece.getAttackingSquares())
        return kingPos in attackedSquares

    def canMoveTo(self, x, y, x1, y1):
        if (old := self.squares[y1][x1]) is not None and old.color == (self.squares[y][x]).color: return False
        self.movePiece(x, y, x1, y1, False)
        returnValue = not self.isKingAttacked(self.squares[y1][x1].color)
        self.squares[y][x] = self.squares[y1][x1]
        self.squares[y1][x1] = old
        self.updatePieceMoves()
        return returnValue

    def checkForWin(self, turn):
        isChecked = self.isKingAttacked(turn)
        for y in range(8):
            for x in range(8):
                if (piece := self.squares[y][x]) is not None and piece.color == turn and \
                        piece.getMovableSquares(self, x, y):
                    return
        return "Checkmate" if isChecked else "Stalemate"

    def scaleImages(self, size):
        for y in range(8):
            for x in range(8):
                if self.squares[y][x] is not None:
                    self.squares[y][x].image = pygame.transform.scale(self.squares[y][x].image, (size, size))

