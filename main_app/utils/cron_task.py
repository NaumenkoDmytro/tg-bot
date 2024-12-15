from time import sleep

from main_app.utils.amazon import Amazon
from main_app.utils.aliexpress import AliExpress
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonAutomationTask, AliExpressAutomationTask, AmazonSavedProducts
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
    directory = f"{settings.BASE_DIR}/storage/"

    for task in tasks:
        try:
            saved_products_send = AmazonSavedProducts.objects.filter(task=task)

            data = [{"image": item.image,
                     "image_path": item.image_path,
                     "product_link": item.image_path,
                     "title": item.title,}
                    for item in saved_products_send]

            bots = init_telegram_bots(task.bot.all())

            for bot in bots:
                for res in data:
                    bot.send_message(res)
            task.status = 'Done'
            task.save()

            for product in saved_products_send:
                product.delete()

            for item in data:
                file_path = os.path.join(directory, item["image_path"].split("/")[-1])
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error Amazon: {e}")


def start_aliexpress_auto_task():
    tasks = AliExpressAutomationTask.objects.filter(status='Approved',
                                                    start_time__gte=timezone.now() - timedelta(hours=2),
                                                    start_time__lte=timezone.now())
    result = []

    for task in tasks:

        aliexpress = AliExpress(app_key=task.aliexpress_api.app_key,
                                secret_key=task.aliexpress_api.secret_key,
                                tracking_id=task.aliexpress_api.tracking_id)

        try:
            curr_page_no = 0

            items = aliexpress.get_products(key_words=task.keywords,
                                            min_price=task.min_price,
                                            max_price=task.max_price,
                                            delivery_days=task.delivery_days,
                                            page_no=curr_page_no, )

            curr_rec_num = items.current_record_count
            total_rec_num = items.total_record_count

            while curr_rec_num <= total_rec_num:
                pprint.pprint(items)
                sleep(2)
                for item in items.products:
                    if item.product_video_url != '':
                        result.append({"title": item.product_title,
                                       "product_link": item.product_detail_url,
                                       "video_url": item.product_video_url,
                                       "price": item.target_sale_price})
                print(len(result))

                result = list({item['title']: item for item in result}.values())

                if len(result) <= task.num_items * 10:
                    curr_page_no += 1
                    items = aliexpress.get_products(key_words=task.keywords,
                                                    min_price=task.min_price,
                                                    max_price=task.max_price,
                                                    delivery_days=task.delivery_days,
                                                    page_no=curr_page_no, )
                    curr_rec_num += items.current_record_count
                    pprint.pprint(items)
                else:
                    break

            result = shuffle_and_return(result, task.num_items) if len(result) >= task.num_items else result

            bots = init_telegram_bots(task.bot.all())

            for bot in bots:
                for res in result:
                    if res["video_url"] is not None:
                        bot.send_video(res)

        except Exception as e:
            print(f"Error AliExpress: {e}")

        task.status = 'Done'
        task.save()
