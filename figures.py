class Piece:
    def __init__(self, color):
        self.name = ""
        self.color = color
    def move(self, board, pos, last_move):
        raise NotImplementedError()

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wp" if color == "white" else "bp"
        self.has_moved = False
    def move(self, board, position, last_move):
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
        if last_move != None and last_move[0].name[1] == "p" and abs(last_move[2][0] - last_move[1][0]) == 2:
            if row == last_move[2][0] and abs(col - last_move[2][1]) == 1:
                if self.color != last_move[0].color:
                    moves.append((row + direction, last_move[2][1]))
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wK" if color == "white" else "bK"
        self.has_moved = False
        self.check = False
    def move(self, board, position, last_move=None):
        moves = []
        row, col = position
        options = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        #if not(self.has_moved): return #рокировка
        for step in options:
            e_row, e_col = row + step[0], col + step[1]
            if within_the_board(e_row, e_col):
                target = board[e_row][e_col]
                if target is None or target.color != self.color:
                    moves.append((e_row, e_col))

        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wq" if color == "white" else "bq"
    def move(self, board, position, last_move=None):
        rook_moves = Rook(self.color).move(board, position, last_move)
        bishop_moves = Bishop(self.color).move(board, position, last_move)
        moves = rook_moves + bishop_moves
        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wn" if color == "white" else "bn"
    def move(self, board, position, last_move=None):
        moves = []
        row, col = position
        options = [(2, -1), (2, 1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, -2), (1, -2)]
        for step in options:
            e_row, e_col = row + step[0], col + step[1]
            if within_the_board(e_row, e_col):
                target = board[e_row][e_col]
                if target is None or target.color != self.color:
                    moves.append((e_row, e_col))
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "wr" if color == "white" else "br"
        self.has_moved = False
    def move(self, board, position, last_move=None):
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
    def move(self, board, position, last_move=None):
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

def real_moves(piece, board, pos, last_move):
    return piece.move(board, pos, last_move)

def within_the_board(row, col):
    return 0 <= row <= 7 and 0 <= col <= 7

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