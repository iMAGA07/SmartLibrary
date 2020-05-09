import datetime
import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('books', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('books.id')),
                                     sqlalchemy.Column('genres', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('genres.id')))


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
