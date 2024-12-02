from django.http import JsonResponse
from main_app.utils.amazon import Amazon
from .utils.telegram_bot import init_telegram_bots
from .models import AmazonAutomationTask
from .utils.img_processing.image_processor import process_image

# Create your views here.

def index(request):
    tasks = AmazonAutomationTask.objects.filter(status='New')
    res = []

    for task in tasks:
        result = []
        amazon = Amazon(access_key=task.amazon_api.access_key,
                        secret_key=task.amazon_api.secret_key,
                        associate_tag=task.amazon_api.partner_tag)

        items = amazon.search_items(keywords=task.keywords,
                                    min_price=task.min_price,
                                    max_price=task.max_price,
                                    item_count=task.num_items).items

        print(items)

        for item in items:
            price = item.offers.listings[0].price.amount
            discount = item.offers.listings[0].price.savings.percentage if item.offers.listings[0].price.savings else 0

            it = {"image": item.images.primary.large.url,
                  "image_path": process_image(item.images.primary.large.url, price, discount),
                  "product_link": item.detail_page_url,
                  "title": item.item_info.title.display_value,}
            result.append(it)

        res.extend(result)
        bots = init_telegram_bots(task.bot.all())

        for bot in bots:
            for res in result:
                bot.send_message(res)

        task.status = 'Done'
        task.save()

    return JsonResponse(res, safe=False)
