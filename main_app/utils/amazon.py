from amazon_paapi import AmazonApi
from tg_bot import settings
from typing import List


class Amazon:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 associate_tag: str):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__associate_tag = associate_tag
        self.__country = settings.AMAZON_COUNTRY
        self.__throttling = settings.AMAZON_THROTTLING
        self.__amazon = AmazonApi(self.__access_key,
                                  self.__secret_key,
                                  self.__associate_tag,
                                  self.__country,
                                  self.__throttling)

    def get_items(self, asins: List[str]):
        return self.__amazon.get_items(asins)

    def search_items(self, keywords: str, min_price:int, max_price:int, item_count: int):
        return self.__amazon.search_items(keywords=keywords,
                                          min_price=min_price,
                                          max_price=max_price,
                                          item_count=item_count)
