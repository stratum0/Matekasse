from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from matekasse import db
from matekasse.models import Item
from matekasse.item.forms import AddItem, EditItem
import os
import secrets
from PIL import Image

item = Blueprint('item', __name__)


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

@item.route("/items", methods=['Post', 'Get'])
def itemoverview():
    additem = AddItem()
    print(additem.validate_on_submit())
    if additem.validate_on_submit():
        newitem = Item(name=additem.name.data, price=additem.price.data)
        if additem.pic.data:
            newitem.imgfile = savePicture(additem.pic.data)
        db.session.add(newitem)
        db.session.commit()
        flash(f'Item {additem.name.data} successfully created!', 'success')
        return redirect(url_for('item.itemoverview'))
    items = Item.query.all()
    return render_template('items.html', additem=additem, item=items)


@item.route("/items/item/<int:item_id>", methods=['Post', 'Get'])
def edititem(item_id):
    moditem = EditItem()
    itm = Item.query.get_or_404(item_id)
    if moditem.validate_on_submit():
        if moditem.delete.data:
            db.session.delete(itm)
        if moditem.submit.data:
            itm.name = moditem.name.data
            itm.price = moditem.price.data
            if moditem.pic.data:
                itm.imgfile = savePicture(moditem.pic.data)
        db.session.commit()
        return redirect(url_for('item.itemoverview'))
    return render_template('edititem.html', moditem=moditem, item=itm)
