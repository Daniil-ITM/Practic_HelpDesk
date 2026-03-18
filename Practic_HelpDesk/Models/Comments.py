from Models.Base import Base
from Models.Users import User
from Models.Tickets import Ticket
from peewee import *
import datetime


class Comment(Base):
    """Модель комментариев"""
    id = AutoField()
    content = TextField()
    user = ForeignKeyField(User, backref='comments', on_delete='CASCADE')
    ticket = ForeignKeyField(Ticket, backref='comments', on_delete='CASCADE')
    is_private = BooleanField(default=False)  # для приватных комментариев
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'comments'