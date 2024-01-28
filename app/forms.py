from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    old_password=PasswordField("Stare haslo", validators=[DataRequired()])
    new_password=PasswordField("Nowe haslo", validators=[DataRequired()])
    confirm_password=PasswordField("Potwierdz haslo", validators=[DataRequired()])

class WarehouseSearchForm(FlaskForm):
    name=StringField("Name")
    model=StringField("Model")

class OfferCreateForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    description=TextAreaField("Name", validators=[DataRequired(), Length(min=1, max=500)])
    date=DateField('Date', format='%Y-%m-%d', default=datetime.utcnow().date)
