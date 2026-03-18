import datetime

from Models.Base import Base
from peewee import *


class User(Base):
    """Модель пользователя"""
    id = AutoField()
    login = CharField(unique=True, max_length=50)
    password_hash = CharField(max_length=255)  # для хранения хеша пароля
    role = CharField(max_length=20, choices=['admin', 'tech', 'user'])
    full_name = CharField(max_length=150, null=True)
    email = CharField(max_length=100, null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'users'