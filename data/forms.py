from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    city_from = StringField('Город', validators=[DataRequired()])
    books_read = StringField('Прочитанные книги')
    books_written = StringField('Написанные книги')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class BookForm(FlaskForm):
    title = StringField("Title")
    about = StringField("About")
    year_published = IntegerField("Year published")
    genre = StringField("Genre")
    submit = SubmitField('Sumbit')


class AddOrderForm(FlaskForm):
    time = StringField("Time of delivery")
    amount = IntegerField("Amount")
    submit = SubmitField('Sumbit')
