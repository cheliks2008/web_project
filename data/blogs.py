import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Blog(SqlAlchemyBase):
    __tablename__ = 'blogs'

    id = sqlalchemy.Column(sqlalchemy.Integer, index=True,
                           primary_key=True, autoincrement=True)
    tutle = sqlalchemy.Column(sqlalchemy.String, unique=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    likes = orm.relationship("Like", back_populates="blog")
