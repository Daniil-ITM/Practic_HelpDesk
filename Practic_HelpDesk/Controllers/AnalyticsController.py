from Models.Tickets import Ticket
from Models.Users import User
from Models.Comments import Comment
from peewee import fn
import datetime


class AnalyticsController:
    '''
    Класс для аналитики
    '''

    @classmethod
    def get_tickets_by_status(cls):
        '''Количество заявок по статусам'''
        stats = {}
        statuses = ['new', 'in_progress', 'resolved', 'closed']
        status_names = {
            'new': 'Новые',
            'in_progress': 'В работе',
            'resolved': 'Решенные',
            'closed': 'Закрытые'
        }

        for status in statuses:
            count = Ticket.select().where(Ticket.status == status).count()
            stats[status_names[status]] = count

        stats['Всего'] = Ticket.select().count()
        return stats

    @classmethod
    def get_tickets_by_user(cls):
        '''Количество заявок по пользователям'''
        result = {}
        users = User.select()
        for user in users:
            count = Ticket.select().where(Ticket.created_by == user).count()
            if count > 0:
                result[user.full_name or user.login] = count
        return result

    @classmethod
    def get_average_resolution_time(cls):
        '''Среднее время решения заявок (в часах)'''
        resolved_tickets = Ticket.select().where(Ticket.status == 'resolved')
        total_time = 0
        count = 0

        for ticket in resolved_tickets:
            if ticket.updated_at and ticket.created_at:
                delta = ticket.updated_at - ticket.created_at
                hours = delta.total_seconds() / 3600
                total_time += hours
                count += 1

        return round(total_time / count, 2) if count > 0 else 0

    @classmethod
    def get_most_active_users(cls, limit=5):
        '''Самые активные пользователи'''
        query = (Ticket
                 .select(Ticket.created_by, fn.COUNT(Ticket.id).alias('count'))
                 .group_by(Ticket.created_by)
                 .order_by(fn.COUNT(Ticket.id).desc())
                 .limit(limit))

        result = []
        for item in query:
            result.append({
                'user': item.created_by.full_name or item.created_by.login,
                'count': item.count
            })
        return result