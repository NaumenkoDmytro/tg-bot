from pprint import pprint
from django.db.models import Q
from django.http import JsonResponse
from main_app.utils.amazon import Amazon
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonAutomationTask, AliExpressAutomationTask, TelegramTestBotConfig
from .img_processing.image_processor import process_image
from .amazon_shorten_link import AmazonShortenLink
from .translator import translate
from .randomize_response import shuffle_and_return
from .aliexpress import AliExpress
import os
from tg_bot import settings


def amazon(obj: AmazonAutomationTask):
    if obj.status == "New":
        res = []

        result = []
        amazon = Amazon(access_key=obj.amazon_api.access_key,
                        secret_key=obj.amazon_api.secret_key,
                        associate_tag=obj.amazon_api.partner_tag)

        amazon_short = AmazonShortenLink(access_key=obj.amazon_api.access_key,
                                         secret_key=obj.amazon_api.secret_key,
                                         associate_tag=obj.amazon_api.partner_tag)

        try:
            i = 1
            items = []

            while i <= 10:
                items.extend(amazon.search_items(keywords=obj.keywords,
                                                 min_price=obj.min_price,
                                                 max_price=obj.max_price,
                                                 item_count=obj.num_items,
                                                 min_reviews_rating=obj.min_reviews_rating,
                                                 min_saving_percent=obj.min_saving_percent,
                                                 item_page=i).items)
                i += 1

            print(len(items))

            items = shuffle_and_return(items, obj.num_items)
            print(items[0])

            for item in items:
                price = item.offers.listings[0].price.amount
                discount = item.offers.listings[0].price.savings.percentage if item.offers.listings[
                    0].price.savings else None

                it = {"image": item.images.primary.large.url,
                          "image_path": process_image(item.images.primary.large.url, price, discount),
                          "product_link": amazon_short.shorten_amazon_link(
                              original_url=f"{item.detail_page_url}?language=pt_PT"),
                          "title": translate(item.item_info.title.display_value).text,}
                result.append(it)

            res.extend(result)

            test_bot = init_telegram_bots(TelegramTestBotConfig.objects.all())[0]

            for res in result:
                res["title"] = "TEST\n\n" + res["title"]
                test_bot.send_message(res)
        except Exception as e:
            print(f"Error: {e}")

        directory = f"{settings.BASE_DIR}/storage/"
        for file in os.listdir(directory):
            if file.endswith(".png"):
                file_path = os.path.join(directory, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


def alik(obj: AliExpressAutomationTask):
    if obj.status == "New":
        res = []
        result = []
        aliexpress = AliExpress(app_key=obj.aliexpress_api.app_key,
                                secret_key=obj.aliexpress_api.secret_key,
                                tracking_id=obj.aliexpress_api.tracking_id)

        try:
            items = aliexpress.get_products(key_words=obj.keywords,
                                            min_price=obj.min_price,
                                            max_price=obj.max_price,
                                            delivery_days=obj.delivery_days, )
            pprint(items.products[0])
            for item in items.products:
                result.append({"title": item.product_title,
                                   "product_link": item.product_detail_url,
                                   "video_url": item.product_video_url if item.product_video_url != '' else None,
                                   "price": item.target_sale_price})
            res.extend(result)

            result = shuffle_and_return(result, obj.num_items)

            test_bot = init_telegram_bots(TelegramTestBotConfig.objects.all())[0]

            for res in result:
                if res["video_url"] is not None:
                    res["title"] = "TEST\n\n" + res["title"]
                    test_bot.send_video(res)
        except Exception as e:
            print(f"Error: {e}")
