from Models.Tickets import Ticket
from Models.Users import User
from Models.Categories import Category
import datetime


class TicketController:
    '''
    Класс для работы с заявками
    Реализация CRUD
    '''

    STATUSES = {
        'new': 'Новая',
        'in_progress': 'В работе',
        'resolved': 'Решена',
        'closed': 'Закрыта'
    }

    @classmethod
    def create(cls, title, description, created_by_id, category_id=None):
        '''
        Создание новой заявки
        '''
        try:
            created_by = User.get_by_id(created_by_id)
            category = Category.get_by_id(category_id) if category_id else None

            ticket = Ticket.create(
                title=title,
                description=description,
                created_by=created_by,
                category=category,
                status='new'
            )
            return {'success': True, 'message': f'Заявка #{ticket.id} создана', 'ticket': ticket}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка создания заявки: {e}'}

    @classmethod
    def get(cls):
        '''
        Получение всех заявок
        '''
        return Ticket.select().order_by(Ticket.created_at.desc())

    @classmethod
    def get_by_id(cls, id):
        '''
        Получение заявки по ID
        '''
        try:
            return Ticket.get_by_id(id)
        except Ticket.DoesNotExist:
            return None

    @classmethod
    def get_by_user(cls, user_id):
        '''
        Получение заявок пользователя
        '''
        return Ticket.select().where(Ticket.created_by == user_id).order_by(Ticket.created_at.desc())

    @classmethod
    def get_by_status(cls, status):
        '''
        Получение заявок по статусу
        '''
        return Ticket.select().where(Ticket.status == status).order_by(Ticket.created_at.desc())

    @classmethod
    def update_status(cls, id, new_status):
        '''
        Обновление статуса заявки
        '''
        try:
            if new_status not in cls.STATUSES:
                return {'success': False, 'message': 'Неверный статус'}

            ticket = Ticket.get_by_id(id)
            old_status = ticket.status
            ticket.status = new_status
            ticket.save()

            return {
                'success': True,
                'message': f'Статус заявки #{id} изменен с {cls.STATUSES[old_status]} на {cls.STATUSES[new_status]}'
            }
        except Exception as e:
            return {'success': False, 'message': f'Ошибка обновления статуса: {e}'}

    @classmethod
    def assign(cls, id, assigned_to_id):
        '''
        Назначение заявки специалисту
        '''
        try:
            ticket = Ticket.get_by_id(id)
            assigned_to = User.get_by_id(assigned_to_id)

            if assigned_to.role not in ['admin', 'tech']:
                return {'success': False, 'message': 'Пользователь не является специалистом'}

            ticket.assigned_to = assigned_to
            ticket.save()

            return {'success': True, 'message': f'Заявка #{id} назначена специалисту {assigned_to.full_name}'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка назначения: {e}'}

    @classmethod
    def search(cls, query):
        '''
        Поиск заявок
        '''
        return Ticket.select().where(
            (Ticket.title.contains(query)) |
            (Ticket.description.contains(query))
        ).order_by(Ticket.created_at.desc())

    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление заявки
        '''
        try:
            ticket = Ticket.get_by_id(id)
            for key, value in kwargs.items():
                if hasattr(ticket, key) and value is not None:
                    setattr(ticket, key, value)
            ticket.save()
            return {'success': True, 'message': f'Заявка #{id} обновлена'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка обновления: {e}'}

    @classmethod
    def delete(cls, id):
        '''
        Удаление заявки
        '''
        try:
            ticket = Ticket.get_by_id(id)
            ticket.delete_instance()
            return {'success': True, 'message': f'Заявка #{id} удалена'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка удаления: {e}'}

    @classmethod
    def get_stats(cls):
        '''
        Получение статистики по заявкам (для аналитики)
        '''
        stats = {}
        for status in cls.STATUSES:
            count = Ticket.select().where(Ticket.status == status).count()
            stats[status] = {
                'count': count,
                'display': cls.STATUSES[status]
            }
        stats['total'] = Ticket.select().count()
        return stats