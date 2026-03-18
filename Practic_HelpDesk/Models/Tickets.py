from Models.Base import Base
from Models.Users import User
from Models.Categories import Category
from peewee import *
import datetime


class Ticket(Base):
    """Модель заявки"""
    id = AutoField()
    title = CharField(max_length=200)
    description = TextField()
    status = CharField(max_length=20, default='new')  # new, in_progress, resolved, closed
    created_by = ForeignKeyField(User, backref='created_tickets', on_delete='CASCADE')
    assigned_to = ForeignKeyField(User, backref='assigned_tickets', null=True, on_delete='SET NULL')
    category = ForeignKeyField(Category, backref='tickets', null=True, on_delete='SET NULL')
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'tickets'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)