from Models.Base import Base
from peewee import *


class Category(Base):
    """Модель категорий"""
    id = AutoField()
    name = CharField(max_length=100)
    type = CharField(max_length=20)  # 'ticket' или 'article'
    description = CharField(max_length=255, null=True)

    class Meta:
        table_name = 'categories'