import random
import copy
import figures
from chess_board import ChessBoard
class ChessBot:
    def __init__(self, color="black", difficulty="very-easy"):
        self.color = color
        self.difficulty = difficulty
        self.board_state = None
        self.has_moved = False

    def set_board(self, board_state):
        if isinstance(board_state, ChessBoard):
            self.board_state = board_state
        else:
            self.board_state = ChessBoard()

    def get_move(self):
        all_moves = self._get_all_possible_moves(self.color)
        if not all_moves:
            return None

        # Проверка, под шахом ли король
        in_check = self.board_state.check_king(self.color)
        if in_check:
            safe_moves = self._get_safe_moves(all_moves)
            if safe_moves:
                # Если есть безопасные ходы, выбираем один случайным образом
                return random.choice(safe_moves)

        # Если король не под шахом, выбираем случайный ход из всех возможных
        return random.choice(all_moves)

    def _get_all_possible_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board_state.board[row][col]
                if piece and piece.color == color:
                    piece_moves = figures.real_moves(piece, self.board_state.board, (row, col), self.board_state.move_history[-1] if self.board_state.move_history else None)
                    for end_pos in piece_moves:
                        if self.board_state._is_safe_move((row, col), end_pos):
                            moves.append(((row, col), end_pos))
        return moves

    def _get_safe_moves(self, all_moves):
        safe_moves = []
        for start, end in all_moves:
            temp_board = copy.deepcopy(self.board_state)
            temp_board.make_move(start, end)
            if not temp_board.check_king(self.color):
                safe_moves.append((start, end))
        return safe_moves

    def _opponent_color(self):
        return "white" if self.color == "black" else "black"

    def format_move_for_uci(self, move):
        if not move:
            return None
        start, end = move
        files = "abcdefgh"
        ranks = "87654321"
        return f"{files[start[1]]}{ranks[start[0]]}{files[end[1]]}{ranks[end[0]]}"
