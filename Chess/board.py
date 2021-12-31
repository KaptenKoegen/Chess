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
        self.enPeasantSquares = None

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
            if self.checkForPromotion(x1, y1):
                return "Promotion"
            if abs(x1 - x) == 2 and self.squares[y1][x1].isKing():
                oldX, newX = (7, 5) if x1 == 6 else (0, 3)
                self.squares[y][newX] = self.squares[y][oldX]
                self.squares[y][oldX] = None
                self.enPeasantSquares = None
            elif isinstance(self.squares[y1][x1], pieces.Pawn):
                if abs(y1 - y) == 2:
                    self.enPeasantSquares = (x1, y1), (x1, y1 - (1 if self.squares[y1][x1].color else -1))
                else:
                    if self.canEnPeasant(x1, y1):
                        temp = self.squares[self.enPeasantSquares[0][1]][self.enPeasantSquares[0][1]]
                        self.squares[self.enPeasantSquares[0][1]][self.enPeasantSquares[0][0]] = None
                    self.enPeasantSquares = None
            else:
                self.enPeasantSquares = None

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

    def checkForPromotion(self, x, y):
        return isinstance(self.squares[y][x], pieces.Pawn) and y in {0, 7}

    def promotePawn(self, x, y, team, piece):
        self.squares[y][x] = self.PIECES[piece](team, piece)

    def canCastle(self, team, x):
        y = ((team + 1) % 2) * 7
        if not (isinstance((king := self.squares[y][4]), pieces.King) and king.color == team and not king.hasMoved and
                isinstance((rook := self.squares[y][x]), pieces.Rook) and rook.color == team and not rook.hasMoved):
            return False
        for x in (range(5, 7) if x == 7 else range(1, 4)):
            if not (self.squares[y][x] is None and self.canMoveTo(4, y, x, y)):
                return False
        return True

    def canEnPeasant(self, x1, y1):
        print(x1, y1)
        print(self.enPeasantSquares)
        return self.enPeasantSquares is not None and (x1, y1) == self.enPeasantSquares[1]



    def scaleImages(self, size):
        for y in range(8):
            for x in range(8):
                if self.squares[y][x] is not None:
                    self.squares[y][x].image = pygame.transform.scale(self.squares[y][x].image, (size, size))

