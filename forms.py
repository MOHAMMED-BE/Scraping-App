from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ],
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ],
    )
    submit = SubmitField("Log In")


class ScrapingForm(FlaskForm):
    product_name = StringField("product_name",
    validators=[DataRequired(),
    Regexp(
            "^[A-Za-z\d]{2,50}$"
        )])
    submit = SubmitField("start scraping data")

class deleteProductForm(FlaskForm):
    submit = SubmitField("delete")
