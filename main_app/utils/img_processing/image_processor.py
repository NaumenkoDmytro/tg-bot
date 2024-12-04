from PIL import Image, ImageDraw, ImageFont
import requests
from django.utils.termcolors import background

from tg_bot.settings import BASE_DIR
import os


def resize_image(image, size=(200, 200)):
    return image.resize(size, Image.Resampling.LANCZOS)


def overlay_on_background(
    foreground_image,
    background_image_path,
    position=(0, 0),
    output_path="result.png",
    discount_percentage=None,
    price_text=None,
    discount_position=(50, 50),
    price_position=(50, 150),
    discount_rotation=0,
    price_rotation=0,
):
    background = Image.open(background_image_path).convert("RGBA")

    background.paste(foreground_image, position, foreground_image)

    if discount_percentage or price_text:
        draw = ImageDraw.Draw(background)

        try:
            font_discount = ImageFont.truetype(os.path.join(BASE_DIR, "main_app", "utils", "img_processing", "norwester.otf"), 40)
            font_price = ImageFont.truetype(os.path.join(BASE_DIR, "main_app", "utils", "img_processing", "norwester.otf"), 50)
        except IOError:
            font_discount = ImageFont.load_default()
            font_price = ImageFont.load_default()

        if discount_percentage:
            discount_text = f"{int(discount_percentage)}%"
            temp_image_discount = Image.new("RGBA", (300, 100), (255, 255, 255, 0))
            temp_draw_discount = ImageDraw.Draw(temp_image_discount)
            temp_draw_discount.text(
                (0, 0), discount_text, fill="White", font=font_discount
            )

            rotated_discount = temp_image_discount.rotate(
                discount_rotation, expand=True
            )

            background.paste(rotated_discount, discount_position, rotated_discount)

        if price_text:
            price_text_formatted = f"{price_text}"

            temp_image_price = Image.new("RGBA", (300, 100), (255, 255, 255, 0))
            temp_draw_price = ImageDraw.Draw(temp_image_price)
            temp_draw_price.text(
                (0, 0), price_text_formatted, fill="black", font=font_price
            )

            rotated_price = temp_image_price.rotate(price_rotation, expand=True)

            background.paste(rotated_price, price_position, rotated_price)

    background.save(output_path)
    print(f"Изображение успешно сохранено как {output_path}")


def process_image(url: str, discounted_price, discount_percentage):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(BASE_DIR, "main_app", "utils", "img_processing", "amazon_image.png"), "wb") as f:
            f.write(response.content)
    else:
        raise Exception("Не удалось загрузить изображение")


    foreground = Image.open(os.path.join(BASE_DIR, "main_app", "utils", "img_processing", "amazon_image.png")).convert("RGBA")

    foreground_resized = resize_image(foreground, size=(500, 600))

    price_text = f"{discounted_price:.2f}"


    if discount_percentage:
        discount_position = (910, 217)
        price_position = (895, 468)
        discount_rotation = 5
        price_rotation = 5
        background = os.path.join(BASE_DIR, "main_app", "utils", "img_processing", "background.png")
    else:
        discount_position = (910, 217)
        price_position = (910, 535)
        discount_rotation = 5
        price_rotation = 5
        background = os.path.join(BASE_DIR, "main_app", "utils", "img_processing", "background_sale.png")



    output_path = f"./storage/output_{url.split('/')[-1].split('.')[0]}.png"

    overlay_on_background(
        foreground_resized,
        background_image_path=background,
        position=(290, 120),
        output_path=output_path,
        discount_percentage=discount_percentage,
        price_text=price_text,
        discount_position=discount_position,
        price_position=price_position,
        discount_rotation=discount_rotation,
        price_rotation=price_rotation,
    )

    return output_path
