from aliexpress_api import AliexpressApi, models
from aliexpress_api.models.request_parameters import LinkType


class AliExpress:
    def __init__(self,
                 app_key: str,
                 secret_key: str,
                 tracking_id: str):
        self.__app_key = app_key
        self.__secret_key = secret_key
        self.__tracking_id = tracking_id
        self.__aliexpress = AliexpressApi(self.__app_key,
                                          self.__secret_key,
                                          models.Language.PT,
                                          models.Currency.EUR,
                                          self.__tracking_id
        )

    def get_items(self, product_keys: list):
        return self.__aliexpress.get_products_details(product_keys)

    def get_products(self,
                     key_words: str,
                     min_price: int,
                     max_price: int,
                     delivery_days: int,
                     page_no: int = 0):
        return self.__aliexpress.get_hotproducts(keywords=key_words,
                                                 max_sale_price=max_price,
                                                 min_sale_price=min_price,
                                                 delivery_days=delivery_days,
                                                 page_size=50,
                                                 ship_to_country="PT",
                                                 page_no=page_no)

    def get_af_link(self, product_id: str):
        return self.__aliexpress.get_affiliate_links(links=[str(product_id)],
                                                     link_type=LinkType.HOTLINK)
