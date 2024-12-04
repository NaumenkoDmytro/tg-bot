from django.http import JsonResponse
from main_app.utils.amazon import Amazon
from .utils.telegram_bot import init_telegram_bots
from .models import AmazonAutomationTask
from .utils.img_processing.image_processor import process_image
from .utils.amazon_shorten_link import AmazonShortenLink
from .utils.translator import translate
import os
from tg_bot import settings


# Create your views here.

def index(request):
    tasks = AmazonAutomationTask.objects.filter(status='New')
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
            items = amazon.search_items(keywords=task.keywords,
                                        min_price=task.min_price,
                                        max_price=task.max_price,
                                        item_count=task.num_items,
                                        min_reviews_rating=task.min_reviews_rating,
                                        min_saving_percent=task.min_saving_percent).items

            print(items)

            for item in items:
                price = item.offers.listings[0].price.amount
                discount = item.offers.listings[0].price.savings.percentage if item.offers.listings[0].price.savings else None

                it = {"image": item.images.primary.large.url,
                      "image_path": process_image(item.images.primary.large.url, price, discount),
                      "product_link": amazon_short.shorten_amazon_link(original_url=f"{item.detail_page_url}?language=pt_PT"),
                      "title": translate(item.item_info.title.display_value).text}
                result.append(it)

            res.extend(result)
            bots = init_telegram_bots(task.bot.all())

            for bot in bots:
                for res in result:
                    bot.send_message(res)
        except Exception as e:
            print(f"Error: {e}")

        task.status = 'Done'
        task.save()

        directory = f"{settings.BASE_DIR}/storage/"
        for file in os.listdir(directory):
            if file.endswith(".png"):
                file_path = os.path.join(directory, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

    return JsonResponse(res, safe=False)
