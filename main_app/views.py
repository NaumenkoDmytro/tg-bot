from copy import deepcopy
from pprint import pprint
from django.db.models import Q
from django.http import JsonResponse
from main_app.utils.amazon import Amazon
from .utils.telegram_bot import init_telegram_bots
from .models import AmazonAutomationTask, AliExpressAutomationTask, TelegramTestBotConfig, AmazonSavedProducts
from .utils.img_processing.image_processor import process_image
from .utils.amazon_shorten_link import AmazonShortenLink
from .utils.translator import translate
from .utils.randomize_response import shuffle_and_return
from .utils.aliexpress import AliExpress
import os
from tg_bot import settings
from time import sleep


# Create your views here.

def amazon(request):
    tasks = AmazonAutomationTask.objects.filter(Q(status='New') | Q(status='Approved'))
    res = []
    directory = f"{settings.BASE_DIR}/storage/"

    print("start")
    for task in tasks:
        bots = init_telegram_bots(task.bot.all())

        if task.status == 'New':
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
                    print(i)
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

                existed_saved_products = AmazonSavedProducts.objects.filter(task=task)

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
                                                                       task=task, )
                    saved_product.save()

                    res["title"] = "TEST\n\n" + res["title"]
                    test_bot.send_message(res)
            except Exception as e:
                print(f"Error: {e}")
        elif task.status == 'Approved':
            saved_products_send = AmazonSavedProducts.objects.filter(task=task)

            data = [{"image": item.image,
                     "image_path": item.image_path,
                     "product_link": item.image_path,
                     "title": item.title,}
                    for item in saved_products_send]
            res = data

            for bot in bots:
                for res in data:
                    bot.send_message(res)
            task.status = 'Done'
            task.save()

            for item in data:
                file_path = os.path.join(directory, item["image_path"].split("/")[-1])
                os.remove(file_path)
                print(f"Deleted: {file_path}")

    return JsonResponse(res, safe=False)


def alik(request):
    tasks = AliExpressAutomationTask.objects.filter(Q(status='New') | Q(status='Approved'))
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
                                            page_no=curr_page_no,)

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

                if len(result) <= task.num_items * 10:
                    curr_page_no += 1
                    items = aliexpress.get_products(key_words=task.keywords,
                                                    min_price=task.min_price,
                                                    max_price=task.max_price,
                                                    delivery_days=task.delivery_days,
                                                    page_no=curr_page_no,)
                    curr_rec_num += items.current_record_count
                    pprint(items)
                else:
                    break

            result = shuffle_and_return(result, task.num_items) if len(result) >= task.num_items else result

            bots = init_telegram_bots(task.bot.all())

            test_bot = init_telegram_bots(TelegramTestBotConfig.objects.all())[0]

            if task.status == 'New':
                for res in result:
                    if res["video_url"] is not None:
                        res["title"] = "TEST\n\n" + res["title"]
                        test_bot.send_video(res)
                        sleep(5)
            elif task.status == 'Approved':
                for bot in bots:
                    for res in result:
                        if res["video_url"] is not None:
                            bot.send_video(res)
                            sleep(5)
                task.status = 'Done'
                task.save()
        except Exception as e:
            print(f"Error: {e}")

    return JsonResponse(result, safe=False)
