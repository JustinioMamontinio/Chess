import figures
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
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != None and piece.color == color:
                    moves = figures.real_moves(piece, self.board, (row, col))
                    attacked.update(moves)
        return attacked



    def set_starting_board(self): #Создаем стартовую доску, расставляем фигуры
        board = [[None] * 8 for _ in range(8)]
        for col in range(8):
            board[6][col] = figures.Pawn("white")
            board[1][col] = figures.Pawn("black")

        board[7][3] = figures.King("white")
        board[0][3] = figures.King("black")

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

        board[7][4] = figures.Queen("white")
        board[0][4] = figures.Queen("black")
        return board

    def make_move(self, start, end): #делаем ход
        s_row, s_col = start  # Стартовая позиция
        e_row, e_col = end  # Конечная позиция
        piece = self.board[s_row][s_col] #Определяем фигуру
        if piece is None: return
        if self.current_player != piece.color: return
        possible_moves = figures.real_moves(piece, self.board, (s_row, s_col))

        if (e_row, e_col) in possible_moves:
            self.board[e_row][e_col] = piece
            self.board[s_row][s_col] = None
            if hasattr(piece, 'has_moved'): piece.has_moved = True #Если у объекта есть такой атрибут, вернет True
            self.move_history.append((piece, start, end))
            self.current_player = "black" if self.current_player == "white" else "white" #Меняем активного игрока
            return True
        return False

    def get_board(self):
        return self.board