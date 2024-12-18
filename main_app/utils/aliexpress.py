from aliexpress_api import AliexpressApi, models
from aliexpress_api.models.request_parameters import LinkType
from time import sleep


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
        res = []
        for product_key in product_keys:
            try:
                res.extend(self.__aliexpress.get_products_details(product_key))
            except Exception as e:
                print(e)
                sleep(10)
                try:
                    res.extend(self.__aliexpress.get_products_details(product_key))
                except Exception as e:
                    print(e)
                    continue
            sleep(10)
        return res

    def get_products(self,
                     key_words: str,
                     min_price: int,
                     max_price: int,
                     page_no: int = 0):
        return self.__aliexpress.get_hotproducts(keywords=key_words,
                                                 max_sale_price=max_price,
                                                 min_sale_price=min_price,
                                                 page_size=50,
                                                 ship_to_country="PT",
                                                 page_no=page_no)

    def get_af_link(self, product_id: str):
        return self.__aliexpress.get_affiliate_links(links=[str(product_id)],
                                                     link_type=LinkType.HOTLINK)
