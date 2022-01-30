from telethon import TelegramClient, events, sync

from resources import configuration as conf


class Telegram_service:
    _instance = None

    api_id = conf.TELEGRAM_API_ID
    api_hash = conf.TELEGRAM_API_HASH
    client = TelegramClient('session_name', api_id, api_hash)

    def __init__(self):
        self.client.start()

    def send_message_to_gpt3(self, text):  # отправка сообщения боту на GPT-3
        self.client.send_message(conf.TELEGRAM_BOT_NAME, text)

    def get_last_message_from_gpt3(self):  # чтение последнего сообщения от бота на GPT-3
        for message in self.client.get_messages(conf.TELEGRAM_BOT_NAME, limit=1):
            return message.message


def telegram_service():
    if Telegram_service._instance is None:
        Telegram_service._instance = Telegram_service()
    return Telegram_service._instance
