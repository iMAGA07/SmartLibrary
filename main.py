import os

import requests
from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_restful import Api
from flask_wtf import FlaskForm
from requests import get
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from data import db_session, users_api
from data.book import Book
from data.db_session import create_session, global_init
from data.forms import LoginForm, RegisterForm, BookForm, AddOrderForm
from data.genre import Genre
from data.orders import Orders

from data.users import User

from flask import make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/library.sqlite")
session = create_session()
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(users_api.blueprint)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    global_init("db/blogs.sqlite")

    if form.validate_on_submit():
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(

                surname=form.surname.data,
                name=form.name.data,
                age=form.age.data,
                city_from=form.city_from.data,
                books_read=form.books_read.data,
                books_written=form.books_written.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
    return render_template('register.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    try:
        os.remove("static/img/map.png")
    except FileNotFoundError:
        pass
    return redirect("/")


@app.route("/")
@app.route("/index")
def index():
    books_read = []
    books_written = []
    message = True
    try:
        if current_user.books_read is not None:
            if len(str(current_user.books_read)) != 0:
                books_read = [int(item) for item in str(current_user.books_read).split(', ')]
        if current_user.books_written is not None:
            if len(str(current_user.books_written)) != 0:
                books_written = [int(item) for item in str(current_user.books_written).split(', ')]
    except AttributeError:
        pass
    books = session.query(Book)
    return render_template('index.html', title="Welcome to SmartLibrary", books=books, books_read=books_read,
                           books_written=books_written)


@app.route('/books/<int:id>', methods=['GET', 'POST'])
def show_book(id):
    book = session.query(Book).filter(Book.id == id).first()
    return render_template('book.html', title='About a book', book=book)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        id = len(session.query(Book).all())
        book = Book()
        book.author = current_user.id
        book.title = form.title.data
        book.about = form.about.data
        book.year_published = form.year_published.data
        if len(current_user.books_written) == 0 or current_user.books_written is None:
            user.books_written += str(id + 1)
        else:
            user.books_written += ', ' + str(id + 1)
        session.add(book)
        session.commit()
        f = request.files['file']
        f.save('static/img/{}.jpg'.format(str(id + 1)))
        return redirect('/')
    return render_template('new_book.html', title='Adding a book',
                           form=form)


@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    form = BookForm()

    session = db_session.create_session()
    book = session.query(Book).filter(Book.id == id).first()
    if book.users.id == current_user.id:
        if request.method == "GET":
            form.title.data = book.title
            form.about.data = book.about
            form.year_published.data = book.year_published
            form.genre.data = book.genre

        if form.validate_on_submit():
            book.author = current_user.id
            book.title = form.title.data
            book.about = form.about.data
            book.year_published = form.year_published.data
            session.add(book)
            session.commit()
            f = request.files['file']
            f.save('static/img/{}.jpg'.format(str(id)))
            return redirect('/')
        return render_template('new_book.html', title='Editing a book',
                               form=form)
    else:
        abort(404)


@app.route('/shopping_cart', methods=['GET', 'POST'])
@login_required
def shopping_cart():
    session = db_session.create_session()
    orders = session.query(Orders).all()
    return render_template("shopping_cart.html", orders=orders)


@app.route('/add_order/<int:id>', methods=['GET', 'POST'])
@login_required
def addorder(id):
    form = AddOrderForm()
    if form.validate_on_submit():
        session = db_session.create_session()

        book = session.query(Book).filter(Book.id == id).first()
        # book.title
        orders = Orders(
            book_title=book.title,
            book_id=book.id,
            time=form.time.data,
            amount=form.amount.data,
            sum=100 * form.amount.data
        )
        session.add(orders)
        session.commit()
        return redirect('/')
    return render_template('add_order.html', title='Adding new order', form=form)


@app.route('/map')
@login_required
def map_show():
    user_city = current_user.city_from

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": user_city,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "Библиотека>",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        # ...
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    print(json_response)
    # Получаем первую найденную организацию.
    organization = json_response["features"][0]
    # Название организации.
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]

    # Получаем координаты ответа.
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    delta = "0.010"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        # позиционируем карту центром на наш исходный адрес
        "ll": ll,
        "spn": ",".join([delta, delta]),
        "l": "map",
        # добавим точку, чтобы указать найденную аптеку
        "pt": "{0},pm2dgl".format(org_point)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    map_file = "static/img/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return render_template('map.html', title='Map')


@app.route('/read_book/<int:id>')
@login_required
def read_book(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()

    if len(user.books_read) == 0 or user.books_read is None:
        user.books_read += str(id)
    else:
        user.books_read += ', ' + str(id)
    session.commit()
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Permission denied'}), 404)


def main():
    app.run()


if __name__ == '__main__':
    main()
