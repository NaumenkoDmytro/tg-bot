import requests
from typing import List

from main_app.models import TelegramBotConfig


class InfoBot:

    def __init__(self, api_token: str, chanel_id: str, is_bot_enable: bool = False):
        self.__IS_BOT_ENABLE = is_bot_enable
        self.__API_TOKEN = api_token
        self.__CHANEL_ID = chanel_id

    @staticmethod
    def __send_message(api_token: str, data = None):
        url = f"https://api.telegram.org/bot{api_token}/sendPhoto"
        print(requests.post(url=url, data=data))

    def send_message(self, data: dict):
        msg = f"""{data['title']}\n\n{data['product_link']}"""

        payload = {
            'chat_id': self.__CHANEL_ID,
            'caption': msg,
            'photo': data['image'],
        }

        self.__send_message(api_token=self.__API_TOKEN, data=payload)
        print("Message sent")


def init_telegram_bots() -> List[InfoBot]:
    telegram_info_bots = []

    bot_credentials = TelegramBotConfig.objects.all()

    if bot_credentials:
        try:
            for bot in bot_credentials:
                telegram_info_bots.append(InfoBot(api_token=bot.bot_api_token,
                                                  chanel_id=bot.channel_id,
                                                  is_bot_enable=bot.is_enabled)
                                          )
        except ValueError as ex:
            print(f"error: {ex}")
    else:
        print('Telegram bots does not configured.')
    return telegram_info_bots
