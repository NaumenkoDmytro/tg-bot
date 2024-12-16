from pprint import pprint
from django.db.models import Q
from django.http import JsonResponse
from main_app.utils.amazon import Amazon
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonAutomationTask, AliExpressAutomationTask, TelegramTestBotConfig, AmazonSavedProducts, AliExpressSavedProducts
from .img_processing.image_processor import process_image
from .amazon_shorten_link import AmazonShortenLink
from .translator import translate
from .randomize_response import shuffle_and_return
from .aliexpress import AliExpress
import os
from tg_bot import settings
from time import sleep


def amazon(obj: AmazonAutomationTask):
    if obj.status == "New":
        directory = f"{settings.BASE_DIR}/storage/"
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

            existed_saved_products = AmazonSavedProducts.objects.filter(task=obj)

            if existed_saved_products:
                for product in existed_saved_products:
                    file_path = os.path.join(directory, product.image_path.split("/")[-1])
                    os.remove(file_path)
                    print(f"Exist image deleted: {file_path}")
                    product.delete()

            for res in result:
                saved_product = AmazonSavedProducts.objects.create(image=res["image"],
                                                                   image_path=res["image_path"],
                                                                   product_link=res["product_link"],
                                                                   title=res["title"],
                                                                   task=obj, )
                saved_product.save()

                res["title"] = "TEST\n\n" + res["title"]
                test_bot.send_message(res)
        except Exception as e:
            print(f"Error: {e}")



def alik(obj: AliExpressAutomationTask):
    if obj.status == "New":
        result = []
        aliexpress = AliExpress(app_key=obj.aliexpress_api.app_key,
                                secret_key=obj.aliexpress_api.secret_key,
                                tracking_id=obj.aliexpress_api.tracking_id)

        try:
            curr_page_no = 0

            items = aliexpress.get_products(key_words=obj.keywords,
                                            min_price=obj.min_price,
                                            max_price=obj.max_price,
                                            delivery_days=obj.delivery_days,
                                            page_no=curr_page_no, )

            curr_rec_num = items.current_record_count
            total_rec_num = items.total_record_count

            while curr_rec_num <= total_rec_num:
                pprint(items)
                sleep(5)
                for item in items.products:
                    if item.product_video_url != '':
                        result.append({"title": item.product_title,
                                       "product_link": item.product_detail_url,
                                       "video_url": item.product_video_url,
                                       "price": item.target_sale_price})
                print(len(result))

                result = list({item['title']: item for item in result}.values())

                if len(result) <= obj.num_items * 10:
                    curr_page_no += 1
                    items = aliexpress.get_products(key_words=obj.keywords,
                                                    min_price=obj.min_price,
                                                    max_price=obj.max_price,
                                                    delivery_days=obj.delivery_days,
                                                    page_no=curr_page_no, )
                    curr_rec_num += items.current_record_count
                    pprint(items)
                else:
                    break

            result = shuffle_and_return(result, obj.num_items) if len(result) >= obj.num_items else result

            test_bot = init_telegram_bots(TelegramTestBotConfig.objects.all())[0]

            existed_saved_products = AliExpressSavedProducts.objects.filter(task=obj)

            if existed_saved_products:
                for product in existed_saved_products:
                    product.delete()

            for res in result:
                saved_product = AliExpressSavedProducts.objects.create(title=res["title"],
                                                                       product_link=res["product_link"],
                                                                       video_url=res["video_url"],
                                                                       price=res["price"],
                                                                       task=obj, )
                saved_product.save()

                res["title"] = "TEST\n\n" + res["title"]
                test_bot.send_video(res)
                sleep(5)
        except Exception as e:
            print(f"Error: {e}")
