from Models.Users import User
import hashlib

class UserController:
    '''
    Класс для работы с пользователями
    Реализация CRUD
    '''

    @classmethod
    def hash_password(cls, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def get(cls):
        '''
        Вывод списка пользователей из таблицы User
        :return: список пользователей (объект)
        '''
        return User.select()

    @classmethod
    def registration(cls, login, password, full_name, email, role='user'):
        '''
        Регистрация нового пользователя
        '''
        try:
            # Проверка существования пользователя
            if User.select().where(User.login == login).exists():
                return {'success': False, 'message': 'Пользователь с таким логином уже существует'}

            user = User.create(
                login=login,
                password_hash=cls.hash_password(password),
                role=role,
                full_name=full_name,
                email=email
            )
            return {'success': True, 'message': f'Пользователь {login} успешно зарегистрирован', 'user': user}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка регистрации: {e}'}

    @classmethod
    def auth(cls, login, password):
        '''
        Аутентификация пользователя
        :param login: логин
        :param password: пароль
        :return: пользователь или None
        '''
        try:
            password_hash = cls.hash_password(password)
            user = User.get(User.login == login, User.password_hash == password_hash)
            return user
        except User.DoesNotExist:
            return None

    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление данных пользователя
        '''
        try:
            user = User.get_by_id(id)
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            user.save()
            return {'success': True, 'message': f'Пользователь {user.login} обновлен'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка обновления: {e}'}

    @classmethod
    def update_status(cls, id):
        '''
        Изменение статуса пользователя (активен/неактивен)
        '''
        try:
            user = User.get_by_id(id)
            user.is_active = not user.is_active
            user.save()
            return {'success': True, 'message': f'Статус пользователя изменен на {user.is_active}'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка изменения статуса: {e}'}

    @classmethod
    def delete(cls, id):
        '''
        Удаление пользователя
        '''
        try:
            user = User.get_by_id(id)
            login = user.login
            user.delete_instance()
            return {'success': True, 'message': f'Пользователь {login} удален'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка удаления: {e}'}

    @classmethod
    def get_by_id(cls, id):
        '''
        Получение пользователя по ID
        '''
        try:
            return User.get_by_id(id)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_by_role(cls, role):
        '''
        Получение пользователей по роли
        '''
        return User.select().where(User.role == role)


