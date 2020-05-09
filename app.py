from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, current_user, UserMixin, login_user
from datetime import datetime
from markupsafe import escape
# from users import User
from forms import LoginForm, RegisterForm


app = Flask(__name__)
app.secret_key = b'secret_key_is_Bekbol_krasavchik'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/register")
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
