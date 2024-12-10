from main_app.utils.amazon import Amazon
from main_app.utils.aliexpress import AliExpress
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonAutomationTask, AliExpressAutomationTask
from django.utils import timezone
from datetime import timedelta
from .amazon_shorten_link import AmazonShortenLink
from .translator import translate
from .img_processing.image_processor import process_image
from .randomize_response import shuffle_and_return
import os
import pprint
from tg_bot import settings


def start_amazon_auto_task():
    tasks = AmazonAutomationTask.objects.filter(status='Approved',
                                                start_time__gte=timezone.now() - timedelta(hours=2),
                                                start_time__lte=timezone.now())
    print(tasks)
    res = []

    for task in tasks:
        result = []
        amazon = Amazon(access_key=task.amazon_api.access_key,
                        secret_key=task.amazon_api.secret_key,
                        associate_tag=task.amazon_api.partner_tag)

        amazon_short = AmazonShortenLink(access_key=task.amazon_api.access_key,
                                         secret_key=task.amazon_api.secret_key,
                                         associate_tag=task.amazon_api.partner_tag)

        try:
            i = 1
            items = []

            while i <= 10:
                items.extend(amazon.search_items(keywords=task.keywords,
                                                 min_price=task.min_price,
                                                 max_price=task.max_price,
                                                 item_count=task.num_items,
                                                 min_reviews_rating=task.min_reviews_rating,
                                                 min_saving_percent=task.min_saving_percent,
                                                 item_page=i).items)
                i += 1

            print(len(items))

            items = shuffle_and_return(items, task.num_items)

            for item in items:
                price = item.offers.listings[0].price.amount
                discount = item.offers.listings[0].price.savings.percentage if item.offers.listings[
                    0].price.savings else None

                it = {"image": item.images.primary.large.url,
                      "image_path": process_image(item.images.primary.large.url, price, discount),
                      "product_link": amazon_short.shorten_amazon_link(
                          original_url=f"{item.detail_page_url}?language=pt_PT"),
                      "title": translate(item.item_info.title.display_value).text}
                result.append(it)

            res.extend(result)
            bots = init_telegram_bots(task.bot.all())

            for bot in bots:
                for res in result:
                    bot.send_message(res)
        except Exception as e:
            print(f"Error Amazon: {e}")

        task.status = 'Done'
        task.save()

        directory = f"{settings.BASE_DIR}/storage/"
        for file in os.listdir(directory):
            if file.endswith(".png"):
                file_path = os.path.join(directory, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


def start_aliexpress_auto_task():
    tasks = AliExpressAutomationTask.objects.filter(status='Approved',
                                                    start_time__gte=timezone.now() - timedelta(hours=2),
                                                    start_time__lte=timezone.now())
    res = []

    for task in tasks:
        result = []

        aliexpress = AliExpress(app_key=task.aliexpress_api.app_key,
                                secret_key=task.aliexpress_api.secret_key,
                                tracking_id=task.aliexpress_api.tracking_id)

        try:
            items = aliexpress.get_products(key_words=task.keywords,
                                            min_price=task.min_price,
                                            max_price=task.max_price,
                                            delivery_days=task.delivery_days, )
            for item in items.products:
                result.append({"title": item.product_title,
                               "product_link": item.product_detail_url,
                               "video_url": item.product_video_url if item.product_video_url != '' else None,
                               "price": item.target_sale_price})
            res.extend(result)
            bots = init_telegram_bots(task.bot.all())

            result = shuffle_and_return(result, task.num_items)

            for bot in bots:
                for res in result:
                    if res["video_url"] is not None:
                        bot.send_video(res)

        except Exception as e:
            print(f"Error AliExpress: {e}")

        task.status = 'Done'
        task.save()
