import io

from PIL import Image, ImageDraw, ImageFont


def draw_caption(img, text, top=False, font_file='data/HelveticaNeue-CondensedBlack.ttf'):
    draw = ImageDraw.Draw(img)
    # Find a suitable font size to fill the entire width:
    w = img.size[0]
    h = 0
    s = 100
    font = ImageFont.truetype(font_file, s)

    while (w >= (img.size[0] - 20)) and s > 12:
        font = ImageFont.truetype(font_file, s)
        w, h = draw.textsize(text, font=font)
        s -= 1

    # Draw the text multiple times in black to get the outline:
    for x in range(-3, 4):
        for y in range(-3, 4):
            draw_y = y if top else img.size[1] - h + y
            draw.text((10 + x, draw_y), text, font=font, fill='black')

    # Draw the text once more in white:
    draw_y = 0 if top else img.size[1] - h
    draw.text((10, draw_y), text, font=font, fill='white')


def get_captioned_image(sentence):
    im = get_image()
    draw_caption(im, sentence, top=True)
    img_io = io.BytesIO()
    im.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)
    return img_io


def get_image():
    return Image.open('images/ez0h1.jpg')
