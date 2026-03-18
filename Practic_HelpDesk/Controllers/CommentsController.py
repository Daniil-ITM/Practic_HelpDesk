from Models.Comments import Comment
from Models.Tickets import Ticket
from Models.Users import User


class CommentController:
    '''
    Класс для работы с комментариями
    '''

    @classmethod
    def create(cls, content, user_id, ticket_id, is_private=False):
        '''
        Создание комментария
        '''
        try:
            user = User.get_by_id(user_id)
            ticket = Ticket.get_by_id(ticket_id)

            # Проверка прав на приватный комментарий
            if is_private and user.role not in ['admin', 'tech']:
                is_private = False

            comment = Comment.create(
                content=content,
                user=user,
                ticket=ticket,
                is_private=is_private
            )
            return {'success': True, 'message': 'Комментарий добавлен', 'comment': comment}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка создания комментария: {e}'}

    @classmethod
    def get_by_ticket(cls, ticket_id, user=None):
        '''
        Получение комментариев к заявке с учетом прав
        '''
        try:
            ticket = Ticket.get_by_id(ticket_id)

            if user and user.role in ['admin', 'tech']:
                # Специалисты и админы видят все комментарии
                return Comment.select().where(Comment.ticket == ticket).order_by(Comment.created_at)
            else:
                # Обычные пользователи видят только публичные
                return Comment.select().where(
                    (Comment.ticket == ticket) &
                    (Comment.is_private == False)
                ).order_by(Comment.created_at)
        except Exception:
            return []

    @classmethod
    def delete(cls, id, user):
        '''
        Удаление комментария
        '''
        try:
            comment = Comment.get_by_id(id)

            # Только автор или админ могут удалить комментарий
            if comment.user.id == user.id or user.role == 'admin':
                comment.delete_instance()
                return {'success': True, 'message': 'Комментарий удален'}
            else:
                return {'success': False, 'message': 'Нет прав на удаление'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка удаления: {e}'}