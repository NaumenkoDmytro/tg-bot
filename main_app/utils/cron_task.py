from main_app.utils.amazon import Amazon
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonAutomationTask
from django.utils import timezone
from datetime import timedelta


def start_amazon_auto_task():
    tasks = AmazonAutomationTask.objects.filter(status='New',
                                                start_time__gte=timezone.now() - timedelta(hours=2),
                                                start_time__lte=timezone.now())
    print(tasks)
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
            result.append({"image": item.images.primary.large.url,
                           "product_link": item.detail_page_url,
                           "title": item.item_info.title.display_value, })
        res.extend(result)
        bots = init_telegram_bots(task.bot.all())

        for bot in bots:
            for res in result:
                bot.send_message(res)

        task.status = 'Done'
        task.save()
