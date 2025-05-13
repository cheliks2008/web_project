import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, index=True,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    blog_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("blogs.id"))
    blog = orm.relationship('Blog')
