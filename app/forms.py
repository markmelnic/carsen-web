from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
