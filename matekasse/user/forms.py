from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from matekasse.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    submit = SubmitField('Sign Up')


class Credit(FlaskForm):
    addzerofive = SubmitField('0,50€')
    addone = SubmitField('1,00€')
    addonefive = SubmitField('1,50€')
    addtwo = SubmitField('2,00€')
    addthree = SubmitField('3,00€')
    addfour = SubmitField('4,00€')
    addfive = SubmitField('5,00€')
    addten = SubmitField('10,00€')
    addtwenty = SubmitField('20,00€')
    addfifty = SubmitField('50,00€')
    remzerofive = SubmitField('0,50€')
    remone = SubmitField('1,00€')
    remonefive = SubmitField('1,50€')
    remtwo = SubmitField('2,00€')
    remthree = SubmitField('3,00€')
    remfour = SubmitField('4,00€')
    remfive = SubmitField('5,00€')
    remten = SubmitField('10,00€')
    remtwenty = SubmitField('20,00€')
    remfifty = SubmitField('50,00€')


class Transfer(FlaskForm):
    beneficary = SelectField('Beneficary')
    transferzerofive = SubmitField('0,50€')
    transferone = SubmitField('1,00€')
    transferonefive = SubmitField('1,50€')
    transfertwo = SubmitField('2,00€')
    transferthree = SubmitField('3,00€')
    transferfour = SubmitField('4,00€')
    transferfive = SubmitField('5,00€')
    transferten = SubmitField('10,00€')

class Edit(FlaskForm):
    rename = StringField('Username', validators=[Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')
