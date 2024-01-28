from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


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