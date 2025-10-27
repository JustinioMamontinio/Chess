from lichess_bot import LichessBot

def load_token():
    with open('bot_credentials.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            if line.startswith('BOT_TOKEN='):
                return line.split('=', 1)[1].strip()
    return None

if __name__ == "__main__":
    token = load_token()
    if not token:
        print("Токен не найден в bot_credentials.txt")
        exit(1)
    bot = LichessBot("very-easy")
    bot.run()
