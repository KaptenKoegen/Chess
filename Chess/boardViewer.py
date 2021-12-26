import pygame
from pygame.locals import *
pygame.init()
from board import Board


class BoardViewer:

    SIZE = 100

    def __init__(self, screen, board):
        self.board: Board = board
        self.screen: pygame.Surface = screen
        self.setup_game()

    def setup_game(self):
        self.selectedSquare: tuple[(int, int)] | None = None
        self.turn: int = 0
        self.timeLeft = [5 * 60 * 1000, 5 * 60 * 1000]  # 5 minutes time
        self.lastTick = pygame.time.get_ticks()
        self.captures = [[], []]
        self.gameStatus = None
        self.board.scaleImages(self.SIZE)

    def update_screen(self):
        self.screen.fill((50, 70, 0))
        self.show_clock(0, self.SIZE * 8)
        self.show_clock(1, self.SIZE * 2)
        for y in range(8):
            for x in range(8):
                color = (255, 255, 255) if not (x + y) % 2 else (50, 70, 0)
                rect = pygame.Rect(x * self.SIZE, (y + 1) * self.SIZE, self.SIZE, self.SIZE)
                pygame.draw.rect(self.screen, color, rect)
                if self.board.getPieceAt(x, y) is not None:
                    self.screen.blit(self.board.getPieceAt(x, y).image, (x * self.SIZE, (y + 1) * self.SIZE))
        self.show_captures(0, self.SIZE * 9)
        self.show_captures(1, 0)
        if self.selectedSquare is not None:
            x, y = self.selectedSquare
            rect = pygame.Rect(x * self.SIZE, (y + 1) * self.SIZE, self.SIZE, self.SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
            for x, y in self.board.getPieceAt(x, y).getMovableSquares(self.board, x, y):
                pygame.draw.circle(self.screen, (127, 127, 127),
                                   (int((x + 0.5) * self.SIZE), int((y + 1.5) * self.SIZE)), self.SIZE // 6)
        if self.gameStatus is not None:
            font = pygame.font.SysFont("Comic Sans", self.SIZE // 2)
            text = font.render(f"{self.gameStatus} !!! click to restart", False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (self.SIZE * 5, self.SIZE * 5)
            pygame.draw.rect(self.screen, (0, 0, 0), rect)
            self.screen.blit(text, rect)
        pygame.display.flip()

    def show_captures(self, player, y):
        for i, piece in enumerate(self.captures[player]):
            self.screen.blit(piece.image, (self.SIZE * 0.7 * i, y))

    def show_clock(self, player, y):
        seconds = self.timeLeft[player] // 1000
        minutes = ("0" + str(seconds // 60))[-2:]
        seconds = ("0" + str(seconds % 60))[-2:]
        text = f"{minutes}: {seconds}"
        font = pygame.font.SysFont('Comic Sans MS', self.SIZE // 2)
        text = font.render(text, False, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (9 * self.SIZE, y)
        self.screen.blit(text, rect)

    def game_loop(self):
        while True:
            self.update_screen()
            if self.gameStatus is None:
                self.timeLeft[self.turn] -= (pygame.time.get_ticks() - self.lastTick)
                self.lastTick = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.gameStatus is not None:
                        self.board = Board()
                        self.setup_game()
                        continue
                    if self.selectedSquare is None:
                        x, y = event.pos[0] // self.SIZE, event.pos[1] // self.SIZE - 1
                        if (piece := self.board.getPieceAt(x, y)) is not None and piece.color == self.turn:
                            self.selectedSquare = x, y
                    else:
                        x, y = self.selectedSquare
                        x1, y1 = event.pos[0] // self.SIZE, event.pos[1] // self.SIZE - 1
                        if (x1, y1) in self.board.getPieceAt(x, y).getMovableSquares(self.board, x, y):
                            piece = self.board.movePiece(x, y, x1, y1)
                            if piece is not None:
                                self.captures[self.turn].append(piece)
                            self.turn = (self.turn + 1) % 2
                            self.gameStatus = self.board.checkForWin(self.turn)

                        self.selectedSquare = None

                    self.update_screen()


def _main():

    size = BoardViewer.SIZE
    screen = pygame.display.set_mode((10 * size, 10 * size))
    board = Board()
    viewer = BoardViewer(screen, board)
    viewer.game_loop()


if __name__ == "__main__":
    _main()
