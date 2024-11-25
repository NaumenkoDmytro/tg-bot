from django.shortcuts import render
from django.http import JsonResponse
from main_app.utils.amazon import Amazon
from .utils.telegram_bot import init_telegram_bots


# Create your views here.

def index(request):
    amazon = Amazon()
    bots = init_telegram_bots()

    items = amazon.get_items(['B07YJDR9PY', 'B09DP2XV1V', 'B0DLWBDPYT'])
    result = []

    for item in items:
        result.append({"image": item.images.primary.large.url,
                       "product_link": item.detail_page_url,
                       "title": item.item_info.title.display_value,})

    for bot in bots:
        for res in result:
            bot.send_message(res)

    return JsonResponse([result], safe=False)
