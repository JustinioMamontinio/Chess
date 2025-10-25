import os

import pygame

import chess_board
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
        self.promotion_menu_visible = False

    def draw_promotion_menu(self):
        if not self.board.promotion_pending:
            return

        row, col, color = self.board.promotion_pending
        screen_col = col + 1
        screen_row = row + 1

        x = screen_col * self.cell_size
        pieces = ['queen', 'rook', 'bishop', 'knight']
        menu_height = len(pieces) * self.cell_size
        menu_y = (screen_row + 1) * self.cell_size

        print(f"Меню: x={x}, y={menu_y}, width={self.cell_size}, height={menu_height}")
        for i, piece_type in enumerate(pieces):
            piece_y = menu_y + i * self.cell_size
            cell_rect = pygame.Rect(x, piece_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)

            piece_symbol = piece_type[0] if i <= 2 else "n"
            piece_name = f"{color[0]}{piece_symbol}"

            if piece_name in self.piece_images:
                self.screen.blit(self.piece_images[piece_name], (x, piece_y))

    def handle_promotion_click(self, pos):
        if not self.board.promotion_pending:
            return False
        x, y = pos
        col = x // self.cell_size
        click_row = y // self.cell_size
        promotion_row, promotion_col, color = self.board.promotion_pending
        screen_col = promotion_col + 1
        screen_row = promotion_row + 1
        if col != screen_col:
            return False
        pieces = ['queen', 'rook', 'bishop', 'knight']
        menu_height = len(pieces) * self.cell_size
        menu_y = (screen_row + 1) * self.cell_size  # Меню под пешкой для белых

        if not (menu_y <= y <= menu_y + menu_height):
            return False

        index = (y - menu_y) // self.cell_size

        if 0 <= index < len(pieces):
            chosen_piece = pieces[index]
            self.board.promote_pawn(chosen_piece)
            return True
        return False

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
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(self.screen, (152, 118, 84), (i * self.cell_size, j * self.cell_size,
                                self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 1)
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color,
                                 ((col+1) * self.cell_size, (row+1) * self.cell_size,
                                  self.cell_size, self.cell_size))

                piece = self.board.board[row][col]
                if piece and piece.name in self.piece_images:  # Проверка наличия изображения
                    self.screen.blit(self.piece_images[piece.name],
                                     ((col+1) * self.cell_size, (row+1) * self.cell_size))

        for row in range(8):
            # Цифра для ряда (ряд row в нашем коде: 0 - верх, 7 - низ)
            # Но мы хотим: внизу 1, вверху 8, поэтому отображаем: для row (0-7) цифра = 8 - row
            number = 8 - row
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(str(number), True, (255, 255, 255))
            # Слева
            x_left = self.cell_size // 2
            y_left = (row + 1) * self.cell_size + self.cell_size // 2
            self.screen.blit(text, (x_left, y_left - text.get_height() // 2))
            # Справа
            x_right = 9 * self.cell_size + self.cell_size // 2
            self.screen.blit(text, (x_right, y_left - text.get_height() // 2))

            # Рисуем буквы снизу и сверху
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for col in range(8):
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(letters[col], True, (255, 255, 255))
            # Снизу
            x_bottom = (col + 1) * self.cell_size + self.cell_size // 2
            y_bottom = 9 * self.cell_size + self.cell_size // 2
            self.screen.blit(text, (x_bottom - text.get_width() // 2, y_bottom))
            # Сверху
            y_top = self.cell_size // 2
            self.screen.blit(text, (x_bottom - text.get_width() // 2, y_top))


    def handle_click(self, pos):
        if self.board.promotion_pending:
            if self.handle_promotion_click(pos):
                return
            self.board.promote_pawn("queen")
            return
        if self.board.promotion_pending:
            if self.handle_promotion_click(pos):
                return
            # Клик мимо меню - превращаем в ферзя по умолчанию
            self.board.promote_pawn("queen")
            return
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        if 1 <= col <= 8 and 1 <= row <= 8:
            b_col = col - 1
            b_row = row - 1
        if self.selected_piece:
            if self.board.make_move(self.selected_piece, (b_row, b_col)):
                self.selected_piece = None
            else:
                self.selected_piece = (b_row, b_col)
        else:
            piece = self.board.board[b_row][b_col]
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (b_row, b_col)
    def close(self):
        pygame.quit()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
            self.screen.fill((0, 0, 0))
            self.draw_board()
            if self.board.promotion_pending:
                self.draw_promotion_menu()
            pygame.display.flip()

        pygame.quit()