import requests
import time
import os

BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"  # ← вставить сюда
TEXT_FILE = "message.txt"
CHAT_ID_FILE = "chat_id.txt"


def load_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            return f.read().strip()
    return None


def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))


def get_chat_id():
    """
    Автоматически получает chat_id.
    Нужно: написать боту любое сообщение.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    print("Ожидаю сообщения от вас боту... Напишите ему что-нибудь.")

    while True:
        r = requests.get(url)
        data = r.json()

        if "result" in data and len(data["result"]) > 0:
            update = data["result"][-1]
            chat = update["message"]["chat"]
            chat_id = chat["id"]
            print("Получен chat_id:", chat_id)
            save_chat_id(chat_id)
            return chat_id

        time.sleep(1)


def send_message(text, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    print("Ответ Telegram:", r.text)


if __name__ == "__main__":
    if BOT_TOKEN == "ВАШ_ТОКЕН_БОТА":
        print("❗ Вставьте токен вашего бота в переменную BOT_TOKEN.")
        exit()

    chat_id = load_chat_id()

    if not chat_id:
        chat_id = get_chat_id()

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read().strip()

    send_message(text, chat_id)
