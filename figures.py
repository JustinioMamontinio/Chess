class Piece:
    def __init__(self, color):
        self.name = ""
        self.color = color
    def move(self, board, pos):
        raise NotImplementedError()

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wp" if color == "white" else "bp"
        self.has_moved = False
    def move(self, board, position):
        moves = []
        row, col = position[0], position[1]
        direction = -1 if self.color == "white" else 1

        if within_the_board(row + direction, col):
            if self.has_moved == False: #первый ход пешки
                if board[row + 2 * direction][col] == None:
                    moves.append((row + 2 * direction, col))
            if board[row + direction][col] == None: #обычный ход
                moves.append((row + direction, col))
        diagonal = [(direction, -1), (direction, 1)]
        for dr, dc in diagonal:
            new_r, new_c = row + dr, col + dc
            if within_the_board(new_r, new_c):
                target = board[new_r][new_c]
                if target != None and target.color != self.color:
                    moves.append((new_r, new_c))
        #Срубить на проходе + превращение в любую фигуру
        return moves
    def check_enemy_king(self, board, position):
        row, col = position[0], position[1]
        direction = -1 if self.color == "white" else 1
        diagonal = [(direction, -1), (direction, 1)]
        for dr, dc in diagonal:
            new_r, new_c = row + dr, col + dc
            if within_the_board(new_r, new_c):
                target = board[new_r][new_c]
                if target != None and target.color != self.color and hasattr(target, "check"):
                    target.check = True

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wK" if color == "white" else "bK"
        self.has_moved = False
        self.check = False
    def move(self, board, position):
        moves = []
        row, col = position
        options = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        #if not(self.has_moved): return #рокировка
        for step in options:
            if within_the_board(row + step[0], col + step[1]):
                moves.append((row + step[0], col + step[1]))
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wq" if color == "white" else "bq"
    def move(self, board, position):
        moves = []
        options = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for step in options:
            row, col = position
            e_row, e_col = row, col
            while within_the_board(e_row + step[0], e_col + step[1]) and board[e_row + step[0]][
                e_col + step[1]] is None:
                e_row, e_col = e_row + step[0], e_col + step[1]
                moves.append((e_row, e_col))
            if within_the_board(e_row + step[0], e_col + step[1]) and board[e_row + step[0]][e_col + step[1]] != None:
                target = board[e_row + step[0]][e_col + step[1]]
                if target.color != self.color:
                    moves.append((e_row + step[0], e_col + step[1]))
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wk" if color == "white" else "bk"
    def move(self, board, position):
        moves = []
        row, col = position
        options = [(2, -1), (2, 1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, -2), (1, -2)]
        for step in options:
            e_row, e_col = row + step[0], col + step[1]
            if within_the_board(e_row, e_col):
                moves.append((e_row, e_col))
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wr" if color == "white" else "br"
        self.has_moved = False
    def move(self, board, position):
        moves = []
        options = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for step in options:
            row, col = position
            e_row, e_col = row, col
            while within_the_board(e_row + step[0], e_col + step[1]) and board[e_row + step[0]][e_col + step[1]] is None:
                e_row, e_col = e_row + step[0], e_col + step[1]
                moves.append((e_row, e_col))
            if within_the_board(e_row + step[0], e_col + step[1]) and board[e_row + step[0]][e_col + step[1]] != None:
                target = board[e_row + step[0]][e_col + step[1]]
                if target.color != self.color:
                    moves.append((e_row + step[0], e_col + step[1]))
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wb" if color == "white" else "bb"
    def move(self, board, position):
        moves = []
        options = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        for step in options:
            row, col = position
            e_row, e_col = row, col
            while within_the_board(e_row + step[0], e_col + step[1]) and board[e_row + step[0]][
                e_col + step[1]] is None:
                e_row, e_col = e_row + step[0], e_col + step[1]
                moves.append((e_row, e_col))
            if within_the_board(e_row + step[0], e_col + step[1]) and board[e_row + step[0]][e_col + step[1]] != None:
                target = board[e_row + step[0]][e_col + step[1]]
                if target.color != self.color:
                    moves.append((e_row + step[0], e_col + step[1]))
        return moves



def real_moves(piece, board, pos):
    return piece.move(board, pos)

def is_move_safe_for_king(board, position, color):
    options = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    row = position[0]
    col = position[1]
 #   for step in options:
#        if within_the_board(row + step[0], col + step[1]):




def within_the_board(row, col):
    return 0 <= row <= 7 and 0 <= col <= 7