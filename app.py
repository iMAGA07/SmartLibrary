from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, current_user, UserMixin, login_user
from datetime import datetime
from markupsafe import escape
from forms import LoginForm, RegisterForm


app = Flask(__name__)
app.secret_key = b'secret_key_is_Bekbol_krasavchik'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #ion = db_session.create_session()
        #user = session.query(User).filter(User.email == form.email.data).first()
        #if user and user.check_password(form.password.data):
            #login_user(user, remember=form.remember_me.data)
            #return redirect("/")
        #return render_template('login.html',
                               #message="Неправильный логин или пароль",
                               #form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    #if form.validate_on_submit():
        #if form.password.data != form.password_again.data:
            #return render_template('register.html', title='Регистрация',
                                   #form=form,
                                   #message="Пароли не совпадают")
        #session = db_session.create_session()
        #if session.query(User).filter(User.email == form.email.data).first():
            #return render_template('register.html', title='Регистрация',
                                   #form=form,
                                   #message="Такой пользователь уже есть")
        #user = User(
            #name=form.name.data,
            #email=form.email.data,
            #about=form.about.data
        #)
        #user.set_password(form.password.data)
        #session.add(user)
        #session.commit()
        #return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == "__main__":
    app.run(debug=True)
