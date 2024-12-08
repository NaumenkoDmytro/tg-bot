from main_app.utils.amazon import Amazon
from .telegram_bot import init_telegram_bots
from main_app.models import AmazonManualTask
from .img_processing.image_processor import process_image
from .translator import translate
import os
from tg_bot import settings


def amazon_manual_process(obj: AmazonManualTask):
    result = []
    amazon = Amazon(access_key=obj.amazon_api.access_key,
                    secret_key=obj.amazon_api.secret_key,
                    associate_tag=obj.amazon_api.partner_tag)

    items = amazon.get_items(obj.asins)

    try:
        for item in items:
            price = item.offers.listings[0].price.amount
            discount = item.offers.listings[0].price.savings.percentage if item.offers.listings[0].price.savings else None

            it = {"image": item.images.primary.large.url,
                  "image_path": process_image(item.images.primary.large.url, price, discount),
                  "product_link": f"{item.detail_page_url}?language=pt_PT",
                  "title": translate(item.item_info.title.display_value).text}
            result.append(it)

            bots = init_telegram_bots(obj.bot.all())

            for bot in bots:
                for res in result:
                    bot.send_message(res)
    except Exception as e:
        print(f"Error: {e}")

    obj.status = 'Done'
    obj.save()

    directory = f"{settings.BASE_DIR}/storage/"
    for file in os.listdir(directory):
        if file.endswith(".png"):
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

    print("Manual Task finished.")
