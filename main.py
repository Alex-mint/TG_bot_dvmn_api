import os
import requests
import telegram
import textwrap
import time
import logging


logger = logging.getLogger('Devman logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message_to_tg(bot, chat_id, new_attempts):
    if new_attempts["is_negative"]:
        text = "К сожалению в работе нашлись ошибки"
    else:
        text = "Преподавателю всё понравилось, можно приступать к работе"

    text = textwrap.dedent(f'''\
    У вас проверили работу "{new_attempts['lesson_title']}"

    {text}
    https://dvmn.org{new_attempts['lesson_url']}''')
    bot.send_message(chat_id=chat_id, text=text)


def main():
    dvmn_token = os.environ["DVMN_TOKEN"]
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    bot = telegram.Bot(token=tg_token)
    headers = {
        "Authorization": f"Token {dvmn_token}",
    }

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Бот запущен')

    params = None
    while True:
        try:
            try:
                response = requests.get("https://dvmn.org/api/long_polling/",
                                        headers=headers, params=params)
                response.raise_for_status()
            except requests.HTTPError:
                time.sleep(5)
                continue
            except ConnectionError:
                time.sleep(5)
                continue
            except requests.exceptions.ReadTimeout:
                continue

            homeworks = response.json()
            if homeworks["status"] == "timeout":
                params = {"timestamp": homeworks["timestamp_to_request"]}
            elif homeworks["status"] == "found":
                new_attempt = homeworks["new_attempts"][0]
                send_message_to_tg(bot, chat_id, new_attempt)
                params = {"timestamp": homeworks["last_attempt_timestamp"]}
        except Exception:
            logger.exception('Бот упал с ошибкой:')


if __name__ == "__main__":
    main()
