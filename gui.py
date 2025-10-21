import os

import pygame
from chess_board import ChessBoard
from figures import Piece
class ChessGUI:
    def __init__(self):
        self.board = ChessBoard()
        self.cell_size = 80
        self.wight = 10 * self.cell_size
        self.height = 10 * self.cell_size
        self.screen = pygame.display.set_mode((self.wight, self.height))
        self.selected_piece = None
        self.load_images()

    def load_images(self):
        self.piece_images = {}
        pieces = ['wp', 'bp', 'wK', 'bK', 'wn', 'bn', 'wr', 'br', 'wb', 'bb', 'wq', 'bq']

        for piece_name in pieces:
            try:
                image_path = os.path.join('images', f'{piece_name}.svg')
                image = pygame.image.load(image_path)
                self.piece_images[piece_name] = pygame.transform.scale(
                    image, (self.cell_size, self.cell_size))
            except:
                surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                if piece_name.startswith('w'):
                    surf.fill((255, 255, 255, 255))  # Белый
                    text_color = (0, 0, 0)
                else:
                    surf.fill((100, 100, 100, 255))  # Серый
                    text_color = (255, 255, 255)
                font = pygame.font.SysFont('Arial', 30)
                symbol = piece_name[1].upper()
                text = font.render(symbol, True, text_color)
                text_rect = text.get_rect(center=(self.cell_size // 2, self.cell_size // 2))
                surf.blit(text, text_rect)
                self.piece_images[piece_name] = surf

    def draw_board(self):
        colors = [(235, 235, 208), (119, 149, 86)]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col + 1) % 2]
                pygame.draw.rect(self.screen, color,
                                 ((col+1) * self.cell_size, (row+1) * self.cell_size,
                                  self.cell_size, self.cell_size))

                piece = self.board.board[row][col]
                if piece and piece.name in self.piece_images:  # Проверка наличия изображения
                    self.screen.blit(self.piece_images[piece.name],
                                     ((col+1) * self.cell_size, (row+1) * self.cell_size))

    def handle_click(self, pos):
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        if 1 <= col <= 8 and 1 <= row <= 8:
            board_col = col - 1
            board_row = row - 1
        if self.selected_piece:
            if self.board.make_move(self.selected_piece, (board_row, board_col)):
                self.selected_piece = None
            else:
                self.selected_piece = (board_row, board_col)
        else:
            piece = self.board.board[board_row][board_col]
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (board_row, board_col)

    def run(self):
        runn = True
        while runn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runn = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()

        pygame.quit()