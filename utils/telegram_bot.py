import requests
from typing import List

from main_app.models import TelegramBotConfig


class InfoBot:

    def __init__(self, api_token: str, chanel_id: str, is_bot_enable: bool = False):
        self.__IS_BOT_ENABLE = is_bot_enable
        self.__API_TOKEN = api_token
        self.__CHANEL_ID = chanel_id

    @staticmethod
    def __send_message(msg: str, api_token: str, chanel_id: str):
        url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chanel_id}&text={msg}"
        requests.post(url=url)

    def send_message(self, data: dict):
        msg = f""""""

        self.__send_message(msg=msg, api_token=self.__API_TOKEN, chanel_id=self.__CHANEL_ID)
        print("Message sent")


def init_telegram_bots() -> List[InfoBot]:
    telegram_info_bots = []

    bot_credentials = TelegramBotConfig.objects.all()

    if bot_credentials:
        try:
            for bot in bot_credentials:
                telegram_info_bots.append(InfoBot(api_token=bot.api_token,
                                                  chanel_id=bot.chanel_id,
                                                  is_bot_enable=bot.is_bot_enable)
                                          )
        except ValueError as ex:
            print(f"error: {ex}")
    else:
        print('Telegram bots does not configured.')
    return telegram_info_bots
