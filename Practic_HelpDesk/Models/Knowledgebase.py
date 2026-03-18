from Models.Base import Base
from Models.Users import User
from Models.Categories import Category
from peewee import *
import datetime


class KnowledgeBase(Base):
    """Модель базы знаний"""
    id = AutoField()
    title = CharField(max_length=200)
    content = TextField()
    category = ForeignKeyField(Category, backref='articles', null=True, on_delete='SET NULL')
    created_by = ForeignKeyField(User, backref='articles', on_delete='CASCADE')
    views = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'knowledge_base'