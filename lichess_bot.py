import time

import berserk
import sys
from chess_board import ChessBoard
from chess_bot import ChessBot

class LichessBot:
    def __init__(self, difficulty):
        # Загружаем токен
        token_file = 'bot_credentials.txt'
        self.token = self._load_token(token_file)
        if not self.token:
            print("Токен не найден или неверный в файле 'bot_credentials.txt'")
            sys.exit(1)

        # Инициализируем сессию и клиента
        self.session = berserk.TokenSession(self.token)
        self.client = berserk.Client(self.session)

        # Инициализация шахматной доски и бота
        self.board = ChessBoard()
        self.bot = ChessBot(color="white", difficulty=difficulty)
        self.bot.set_board(self.board)

    def _load_token(self, token_file):
        try:
            with open(token_file, 'r',
                      encoding='utf-8-sig') as file: # Используем 'utf-8-sig' для автоматического удаления BOM
                token_line = file.readline().strip()
                if token_line.startswith('BOT_TOKEN='):
                    return token_line.split('=')[1].strip()
        except Exception as e:
            print(f"Ошибка при чтении токена из файла {token_file}: {e}")
        return None

    def uci_to_coords(self, uci_move):
        if len(uci_move) < 4:
            return None

        file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        rank_map = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}

        try:
            start = (rank_map[uci_move[1]], file_map[uci_move[0]])
            end = (rank_map[uci_move[3]], file_map[uci_move[2]])
            return start, end
        except KeyError as e:
            print(f"Ошибка при конвертации {uci_move}: {e}")
            return None

    def coords_to_uci(self, start, end):
        file_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        rank_map = {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'}

        try:
            move_uci = f"{file_map[start[1]]}{rank_map[start[0]]}{file_map[end[1]]}{rank_map[end[0]]}"
            return move_uci
        except KeyError as e:
            print(f"Ошибка при конвертации координат: {start}->{end}, ошибка: {e}")
            return None

    def handle_game_state(self, game_id, game_state):
        print(f"Обрабатываем игру {game_id}")

        moves = game_state.get('moves', '').split()
        if not moves:
            print("Нет ходов в состоянии игры")
            return

        our_color = None
        game_info = self.client.games.export(game_id)

        if game_info.get('players', {}).get('white', {}).get('user', {}).get('name') == self.client.account.get()['username']:
            our_color = 'white'
        else:
            our_color = 'black'

        print(f"Цвет бота: {our_color}")

        if len(moves) % 2 == 0:
            current_turn = 'white'
        else:
            current_turn = 'black'

        if current_turn != our_color:
            print(f"Ожидаем ход {current_turn}")
            return

        print(f"Ход бота! Всего ходов: {len(moves)}")

        self.board = ChessBoard()
        self.bot.set_board(self.board)

        for move_uci in moves:
            coords = self.uci_to_coords(move_uci)
            if coords:
                start, end = coords
                success = self.board.make_move(start, end)

                if not success:
                    print(f"Ошибка при применении хода {move_uci}")
                    if len(move_uci) == 5 and self.board.promotion_pending:
                        promo_piece = move_uci[4]
                        promo_map = {'q': 'queen', 'r': 'rook', 'b': 'bishop', 'n': 'knight'}
                        piece_type = promo_map.get(promo_piece, 'queen')
                        self.board.promote_pawn(piece_type)

        bot_move = self.bot.get_move()

        if bot_move:
            start_coords, end_coords = bot_move
            move_uci = self.coords_to_uci(start_coords, end_coords)

            piece = self.board.board[start_coords[0]][start_coords[1]]
            from figures import Pawn
            if isinstance(piece, Pawn) and (end_coords[0] == 0 or end_coords[0] == 7):
                move_uci += 'q'

            if move_uci:
                print(f"Бот делает ход: {move_uci}")

                try:
                    self.client.bots.make_move(game_id, move_uci)
                    print(f"Ход отправлен: {move_uci}")
                except Exception as e:
                    print(f"Ошибка при отправке хода: {e}")
            else:
                print("Ошибка при конвертации хода бота в UCI")
        else:
            print("Бот не может найти ход!")

    def run(self):
        """Основной цикл работы бота"""
        print("=" * 50)
        print("Бот для Lichess запущен")
        print("=" * 50)

        print("Ожидаем событий...")

        try:
            account = self.client.account.get()
            print(f"Имя бота: {account['username']}")
            print(f"Ссылка: https://lichess.org/@{account['username']}")
        except Exception as e:
            print(f"Ошибка при получении данных аккаунта: {e}")
            return

        # Обработка событий
        for event in self.client.bots.stream_incoming_events():
            print(f"\nПолучено событие: {event['type']}")

            if event['type'] == 'challenge':
                challenge = event['challenge']
                challenge_id = challenge['id']
                challenger = challenge['challenger']['name']

                print(f"Вызов от {challenger} (ID: {challenge_id})")

                try:
                    self.client.bots.accept_challenge(challenge_id)
                    print(f"Вызов принят")
                except Exception as e:
                    print(f"Ошибка при принятии вызова: {e}")

            elif event['type'] == 'gameStart':
                game_id = event['game']['id']
                print(f"Началась игра: {game_id}")
                print(f"Ссылка: https://lichess.org/{game_id}")

                self.handle_game_stream(game_id)

    def handle_game_stream(self, game_id):
        """Обрабатывает поток событий игры"""
        print(f"Начинаем обработку игры {game_id}")
        time.sleep(2)
        try:
            for event in self.client.bots.stream_game_state(game_id):
                if event['type'] == 'gameFull':
                    print("Получено полное состояние игры")
                    self.handle_game_state(game_id, event['state'])

                elif event['type'] == 'gameState':
                    print(f"Обновление состояния игры, статус: {event.get('status', 'неизвестно')}")

                    if event.get('status') == 'started':
                        self.handle_game_state(game_id, event)
                    else:
                        print(f"Игра окончена: {event.get('status')}")
                        if 'winner' in event:
                            winner = event['winner']
                            print(f"Победитель: {'белые' if winner == 'white' else 'черные'}")
                        break

                elif event['type'] == 'chatLine':
                    username = event['username']
                    text = event['text']
                    print(f"{username}: {text}")

        except Exception as e:
            print(f"Ошибка при обработке игры: {e}")
