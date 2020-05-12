import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Orders(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'
    order_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    book_id = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.String)
    book_title = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("books.title"))
    amount = sqlalchemy.Column(sqlalchemy.Integer)
    sum = sqlalchemy.Column(sqlalchemy.Integer)
    book = orm.relation("Book")