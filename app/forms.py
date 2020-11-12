from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    # remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password"), Length(min=8)],
    )
    submit = SubmitField("Sign up")

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError("Email already in use, please choose another")

class SearchForm(FlaskForm):
    manufacturer = StringField("Manufacturer", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])

    price_from = IntegerField("From", validators=[])
    price_to = IntegerField("To", validators=[])

    reg_from = IntegerField("From", validators=[])
    reg_to = IntegerField("To", validators=[])

    mileage_from = IntegerField("From", validators=[])
    mileage_to = IntegerField("To", validators=[])

    submit = SubmitField("Search")