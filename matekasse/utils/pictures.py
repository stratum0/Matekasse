import os
import secrets
from PIL import Image
from flask import current_app


def savePicture(pic):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/item_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def delPicture(pic):
    os.remove(os.path.join(current_app.root_path, 'static/item_pics', pic))
