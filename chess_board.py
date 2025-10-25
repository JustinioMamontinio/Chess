import figures
import sys
class ChessBoard:
    def __init__(self): #Задаем базовые настройки доски и игры в целом
        self.board = self.set_starting_board()
        self.current_player = "white"
        self.move_history = []
        self.check = False
        self.attacked_squares = {"white":set(), "black":set()}
        self._update_attacked_squares()
        self.promotion_pending = None

    def _update_attacked_squares(self):
        self.attacked_squares["white"] = self._get_attacked_squares("white")
        self.attacked_squares["black"] = self._get_attacked_squares("black")

    def _get_attacked_squares(self, color): #Получаем  поля, которые находятся под ударом
        attacked = set()
        last_move = self.move_history[-1] if self.move_history else None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != None and piece.color == color:
                    moves = figures.real_moves(piece, self.board, (row, col), last_move)
                    attacked.update(moves)
        return attacked

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == color:
                        if isinstance(piece, figures.King):
                            return (row, col)



    def set_starting_board(self): #Создаем стартовую доску, расставляем фигуры
        board = [[None] * 8 for _ in range(8)]
        for col in range(8):
            board[6][col] = figures.Pawn("white")
            board[1][col] = figures.Pawn("black")

        board[7][4] = figures.King("white")
        board[0][4] = figures.King("black")

        board[7][1] = figures.Knight("white")
        board[7][6] = figures.Knight("white")
        board[0][1] = figures.Knight("black")
        board[0][6] = figures.Knight("black")

        board[7][0] = figures.Rook("white")
        board[7][7] = figures.Rook("white")
        board[0][0] = figures.Rook("black")
        board[0][7] = figures.Rook("black")

        board[7][2] = figures.Bishop("white")
        board[7][5] = figures.Bishop("white")
        board[0][2] = figures.Bishop("black")
        board[0][5] = figures.Bishop("black")

        board[7][3] = figures.Queen("white")
        board[0][3] = figures.Queen("black")
        return board

    def make_move(self, start, end): #делаем ход

        s_row, s_col = start  # Стартовая позиция
        e_row, e_col = end  # Конечная позиция
        piece = self.board[s_row][s_col] #Определяем фигуру
        print(f"Ход: {start} -> {end}, фигура: {piece.name if piece else 'None'}")
        if piece is None: return
        if self.current_player != piece.color: return
        self.find_king(self.current_player)
        enemy_color = 'black' if self.current_player == 'white' else 'white'
        last_move = self.move_history[-1] if self.move_history else None
        possible_moves = figures.real_moves(piece, self.board, (s_row, s_col), last_move)

        if (e_row, e_col) in possible_moves:
            if not self._is_safe_move(start, end):
                return False  # Ход оставляет короля под шахом
            if (isinstance(piece, figures.Pawn) and last_move and isinstance(last_move[0], figures.Pawn) and abs(e_col - s_col) == 1
                    and abs(last_move[2][0] - last_move[1][0]) == 2 and last_move[2][0] == s_row): #Взятие на проходе
                self.board[s_row][e_col] = None
            if isinstance(piece, figures.King) and abs(e_col - s_col) == 2 and not(piece.check): #Рокировка
                if e_col - s_col == -2:
                    self.board[s_row][3] = self.board[s_row][0]
                    self.board[s_row][0] = None
                elif e_col - s_col == 2:
                    self.board[s_row][5] = self.board[s_row][7]
                    self.board[s_row][7] = None
            self.board[e_row][e_col] = piece
            self.board[s_row][s_col] = None
            if hasattr(piece, 'has_moved'): piece.has_moved = True #Если у объекта есть такой атрибут, вернет True
            self.move_history.append((piece, start, end))
            self.last_move = (piece, start, end)
            if isinstance(piece, figures.Pawn) and (e_row == 0 or e_row == 7):
                self.promotion_pending = (e_row, e_col, piece.color)
            else:
                self.current_player = "black" if self.current_player == "white" else "white"
            self._update_attacked_squares()
            pos_enemy_king = self.find_king(enemy_color)
            if self.board[pos_enemy_king[0]][pos_enemy_king[1]] in self.attacked_squares[piece.color]: print(f'{enemy_color} король попал под шах')
            if self.checkmate(enemy_color) or self.stalemate(enemy_color):
                print('Игра окончена')

            return True
        return False

    def promote_pawn(self, piece_type):
        row, col, color = self.promotion_pending
        if piece_type == "queen":
            new_piece = figures.Queen(color)
        elif piece_type == "rook":
            new_piece = figures.Rook(color)
        elif piece_type == "bishop":
            new_piece = figures.Bishop(color)
        elif piece_type == "knight":
            new_piece = figures.Knight(color)
        else:
            new_piece = figures.Queen(color)  # По умолчанию ферзь

        self.board[row][col] = new_piece
        self.promotion_pending = None
        self.current_player = "black" if self.current_player == "white" else "white"
        return True

    def stalemate(self, color):

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    moves = (figures.real_moves(piece, self.board, (row, col), self.last_move))
                    for i in moves:
                        if self._is_safe_move((row, col), i): return False
        print(f"Пат, {color} нечем ходить")
        return True

    def check_king(self, color):
        pos = self.find_king(color)
        row, col = pos[0], pos[1]
        king = self.board[row][col]
        self._update_attacked_squares()
        if color == 'white':
            is_in_check = (row, col) in self.attacked_squares['black']
        else:
            is_in_check = (row, col) in self.attacked_squares['white']
        if hasattr(king, 'check'):
            king.check = is_in_check
        if is_in_check:
            print(f'{color} король попал под шах')
        return is_in_check

    def checkmate(self, color):
        if not self.check_king(color):
            return False
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board[start_row][start_col]
                if piece and piece.color == color:
                    moves = figures.real_moves(piece, self.board, (start_row, start_col), last_move=None)

                    for end_row, end_col in moves:
                        # Пробуем сделать ход
                        if self._is_safe_move((start_row, start_col), (end_row, end_col)):
                            return False  # Нашелся безопасный ход - не мат

        print(f'Мат! Победили {"белые" if color == "black" else "черные"}')
        return True

    def _is_safe_move(self, start, end): #не оставляет ли ход короля под шахом
        s_row, s_col = start
        e_row, e_col = end
        piece = self.board[s_row][s_col]
        color = piece.color
        original_piece = self.board[e_row][e_col]

        self.board[e_row][e_col] = piece #Временный ход
        self.board[s_row][s_col] = None
        still_in_check = self.check_king(color)

        self.board[s_row][s_col] = piece # Откатываем ход
        self.board[e_row][e_col] = original_piece

        return not still_in_check

    def get_board(self):
        return self.board