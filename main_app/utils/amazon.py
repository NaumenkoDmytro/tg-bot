from amazon_paapi import AmazonApi
from tg_bot import settings
from typing import List


class Amazon:
    def __init__(self):
        self.__access_key = settings.AMAZON_ACCESS_KEY
        self.__secret_key = settings.AMAZON_SECRET_KEY
        self.__associate_tag = settings.AMAZON_ASSOCIATE_TAG
        self.__country = settings.AMAZON_COUNTRY
        self.__throttling = settings.AMAZON_THROTTLING
        self.__amazon = AmazonApi(self.__access_key,
                                  self.__secret_key,
                                  self.__associate_tag,
                                  self.__country,
                                  self.__throttling)

    def get_items(self, asins: List[str]):
        return self.__amazon.get_items(asins)
