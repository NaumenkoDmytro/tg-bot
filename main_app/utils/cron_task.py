from time import sleep

from main_app.utils.amazon import Amazon
from main_app.utils.aliexpress import AliExpress
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonAutomationTask, AliExpressAutomationTask, AmazonSavedProducts, AliExpressSavedProducts
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
                     "product_link": item.product_link,
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

    for task in tasks:
        bots = init_telegram_bots(task.bot.all())

        try:
            saved_products_send = AliExpressSavedProducts.objects.filter(task=task)

            data = [{"title": item.title,
                     "product_link": item.product_link,
                     "video_url": item.video_url,
                     "price": item.price, }
                    for item in saved_products_send]

            for bot in bots:
                for res in data:
                    bot.send_video(res)
                    sleep(5)
            task.status = 'Done'
            task.save()
        except Exception as e:
            print(f"Error AliExpress: {e}")
