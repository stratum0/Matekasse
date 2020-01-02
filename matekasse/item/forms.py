from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, FileField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed


class AddItem(FlaskForm):
    name = StringField('Item', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Item"})
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    pic = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Item')


class EditItem(FlaskForm):
    name = StringField('Item', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Item"})
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    pic = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Edit Item')
    delete = SubmitField('Delete')
