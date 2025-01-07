import requests
from typing import List

from main_app.models import TelegramBotConfig


class InfoBot:

    def __init__(self, api_token: str,
                 chanel_id: str,
                 chanel_name: str,
                 chanel_link: str,
                 is_bot_enable: bool = False,
                 ):
        self.__IS_BOT_ENABLE = is_bot_enable
        self.__API_TOKEN = api_token
        self.__CHANEL_ID = chanel_id
        self.chanel_name = chanel_name
        self.chanel_link = chanel_link

    @staticmethod
    def __send_message(api_token: str, data = None, files=None):
        url = f"https://api.telegram.org/bot{api_token}/sendPhoto"
        print(requests.post(url=url, data=data, files=files))

    @staticmethod
    def __send_message_video(api_token: str, data=None, files=None):
        url = f"https://api.telegram.org/bot{api_token}/sendVideo"
        print(requests.post(url=url, data=data, files=files))

    def send_video(self, data: dict):
        msg = (f"{data['title']}\n\n"
               f"🔗 <a href='{data['product_link']}'>Link do produto</a>\n\n"
               f"📩 <a href='{self.chanel_link}'>{self.chanel_name}</a>"
               )

        payload = {
            'chat_id': self.__CHANEL_ID,
            'caption': msg,
            'video': data['video_url'],
            'parse_mode': 'HTML',
            'disable_notification': True
        }
        self.__send_message_video(api_token=self.__API_TOKEN, data=payload)
        print("Message sent")

    def send_message(self, data: dict):
        msg = (f"{data['title']}\n\n"
        f"🔗 <a href='{data['product_link']}'>Link do produto</a>\n\n"
        f"📩 <a href='{self.chanel_link}'>{self.chanel_name}</a>"
        )

        if 'image_path' in data and data['image_path']:
            with open(data['image_path'], 'rb') as image_file:
                payload = {
                    'chat_id': self.__CHANEL_ID,
                    'caption': msg,
                    'parse_mode': 'HTML',
                    'disable_notification': True
                }
                files = {
                    'photo': image_file,
                }
                self.__send_message(api_token=self.__API_TOKEN, data=payload, files=files)
        else:
            # For URL-based images
            payload = {
                'chat_id': self.__CHANEL_ID,
                'caption': msg,
                'photo': data['image'],
                'parse_mode': 'markdown',
                'disable_notification': True
            }
            self.__send_message(api_token=self.__API_TOKEN, data=payload)
        print("Message sent")


def init_telegram_bots(bot_credentials) -> List[InfoBot]:
    telegram_info_bots = []

    if bot_credentials:
        try:
            for bot in bot_credentials:
                if bot.is_enabled:
                    telegram_info_bots.append(InfoBot(api_token=bot.bot_api_token,
                                                      chanel_id=bot.channel_id,
                                                      is_bot_enable=bot.is_enabled,
                                                      chanel_name=bot.channel_name,
                                                      chanel_link=bot.channel_link,)
                                              )
        except ValueError as ex:
            print(f"error: {ex}")
    else:
        print('Telegram bots does not configured.')
    return telegram_info_bots
