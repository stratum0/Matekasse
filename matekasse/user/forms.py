from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length
from matekasse.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    submit = SubmitField('Sign Up')


class Transfer(FlaskForm):
    beneficary = SelectField('Beneficary')
    sum = SelectField('Sum')
    transfer = SubmitField('Transfer')


class Edit(FlaskForm):
    rename = StringField('Username', validators=[Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')
