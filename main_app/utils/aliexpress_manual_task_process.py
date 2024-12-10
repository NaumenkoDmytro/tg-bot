from .aliexpress import AliExpress
from main_app.models import AliExpressManualTask, TelegramTestBotConfig
from .telegram_bot import init_telegram_bots


def ali_manual_process(obj: AliExpressManualTask):
    result = []
    aliexpress = AliExpress(app_key=obj.aliexpress_api.app_key,
                            secret_key=obj.aliexpress_api.secret_key,
                            tracking_id=obj.aliexpress_api.tracking_id)

    items = aliexpress.get_items(product_keys=obj.product_codes)

    try:
        for item in items:
            print(item)
            result.append({"title": item.product_title,
                           "product_link": item.promotion_link,
                           "video_url": item.product_video_url if item.product_video_url != '' else None,
                           "price": item.original_price,})

        bots = init_telegram_bots(obj.bot.all())
        test_bot = init_telegram_bots(TelegramTestBotConfig.objects.all())[0]

        if obj.status == 'New':
            for res in result:
                if res["video_url"] is not None:
                    res["title"] = "TEST\n\n" + res["title"]
                    test_bot.send_video(res)
        elif obj.status == 'Approved':
            for bot in bots:
                for res in result:
                    if res["video_url"] is not None:
                        bot.send_video(res)
            obj.status = 'Done'
            obj.save()
        print("Manual Task finished.")
    except Exception as e:
        print(f"Error: {e}")
