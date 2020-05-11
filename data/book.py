import datetime
import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    year_published = sqlalchemy.Column(sqlalchemy.Integer)
    about = sqlalchemy.Column(sqlalchemy.String)
    genre = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("genres.id"))
    users = orm.relation('User')

    genres = orm.relation("Genre")
