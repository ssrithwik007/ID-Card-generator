from PIL import Image, ImageDraw, ImageFont
import textwrap, os
from io import BytesIO

base_dir = os.path.dirname(__file__)
image = Image.open(os.path.join(base_dir, "assets/id_card_template.png")).convert("RGBA")
text_font = ImageFont.truetype(os.path.join(base_dir, "assets/ComicRelief-Regular.ttf"), 30)
title_font = ImageFont.truetype(os.path.join(base_dir, "assets/ComicRelief-Regular.ttf"), 60)
info_font = ImageFont.truetype(os.path.join(base_dir, "assets/ComicRelief-Regular.ttf"), 20)
sign_font = ImageFont.truetype(os.path.join(base_dir, "assets/Signatie.otf"), 40)

def generate(data):
    #
    # Create a copy of the base image
    image_copy = image.copy()
    # Create a drawing context
    draw = ImageDraw.Draw(image_copy)

    #Create an Image object of the user's photo and resize it
    user_image = Image.open(data["photo"]).convert("RGBA").resize((280, 280))
    # Paste the user's photo onto the image
    image_copy.paste(user_image, (74, 240))

    spl_info_lines = textwrap.wrap(data["spl_info"], width=50)
    spl_info = "\n".join(spl_info_lines)
    draw.multiline_text((447,376), spl_info, (0, 0, 0), font=info_font)

    texts = [
        (data["title"], (508, 33), title_font),
        (data["name"], (748, 145), text_font),
        (data["dob"], (829, 205), text_font),
        (data["place"], (748, 266), text_font),
        (data["ph_no"], (776, 327), text_font),
        (data["name"], (748, 531), sign_font)
    ]

    for text, position, font in texts:
        text_w = draw.textlength(text, font=font)
        pos = (position[0] - text_w // 2, position[1])
        draw.text(pos, text, (0, 0, 0), font=font)

    icon_path = os.path.join(base_dir, f"assets/icons/icon_{data['icon']}.png")
    icon_image = Image.open(icon_path).convert("RGBA").resize((300, 300))
    icon_data = icon_image.getdata()
    new_icon_data = []

    for item in icon_data:
        new_icon_data.append((item[0], item[1], item[2], int(0.4*item[3])))

    icon_image.putdata(new_icon_data)

    image_copy.paste(icon_image, (550, 230), icon_image)

    buffer = BytesIO()
    image_copy.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()