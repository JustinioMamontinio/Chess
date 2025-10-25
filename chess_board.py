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

        if piece is None: return
        if self.current_player != piece.color: return
        self.find_king(self.current_player)
        enemy_color = 'black' if self.current_player == 'white' else 'white'
        last_move = self.move_history[-1] if self.move_history else None
        possible_moves = figures.real_moves(piece, self.board, (s_row, s_col), last_move)

        if (e_row, e_col) in possible_moves:
            if not self._is_safe_move(start, end):
                return False  # Ход оставляет короля под шахом
            if piece.name[1] == "p" and self.board[e_row][e_col] == None and abs(e_col - s_col) == 1: #Взятие на проходе
                self.board[s_row][e_col] = None
            self.board[e_row][e_col] = piece
            self.board[s_row][s_col] = None
            if hasattr(piece, 'has_moved'): piece.has_moved = True #Если у объекта есть такой атрибут, вернет True
            self.move_history.append((piece, start, end))
            self.last_move = (piece, start, end)
            self._update_attacked_squares()
            if self.checkmate(enemy_color):
                print('Игра окончена')
                sys.exit()
            self.current_player = "black" if self.current_player == "white" else "white" #Меняем активного игрока

            return True
        return False

    def check_king(self, color):
        pos = self.find_king(color)
        row, col = pos[0], pos[1]
        king = self.board[row][col]
        self._update_attacked_squares()
        if color == 'white':
            is_in_check = (row, col) in self.attacked_squares['black']
        else:
            is_in_check = (row, col) in self.attacked_squares['white']
        if hasattr(king, 'check'): king.check = is_in_check
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