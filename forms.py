from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField

#<p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>

class LoginForm(FlaskForm):
   email = EmailField('Почта', validators=[DataRequired()])
   password = PasswordField('Пароль', validators=[DataRequired()])
   #remember_me =
   submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
   surname = StringField('Фамилия', validators=[DataRequired()])
   name = StringField('Имя', validators=[DataRequired()])
   age = StringField('Возраст', validators=[DataRequired()])
   city_from = StringField('Город', validators=[DataRequired()])
   books_read = StringField('Прочитанные книги', validators=[DataRequired()])
   books_written = StringField('Написанные книги', validators=[DataRequired()])
   email = EmailField('Почта', validators=[DataRequired()])
   hashed_password = PasswordField('Пароль', validators=[DataRequired()])
   modified_date = PasswordField('Дата', validators=[DataRequired()])
   submit = SubmitField('Зарегистрироваться')
   