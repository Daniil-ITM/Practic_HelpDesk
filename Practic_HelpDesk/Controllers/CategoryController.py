from Models.Categories import Category

class CategoryController:
    '''
    Класс для работы с категориями
    Реализация CRUD
    '''

    @classmethod
    def create(cls, name, type='ticket', description=None):
        '''
        Создание новой категории
        '''
        try:
            category = Category.create(
                name=name,
                type=type,
                description=description
            )
            return {'success': True, 'message': f'Категория {name} создана', 'category': category}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка создания категории: {e}'}

    @classmethod
    def get(cls):
        '''
        Вывод списка категорий
        '''
        return Category.select()

    @classmethod
    def get_by_type(cls, type):
        '''
        Получение категорий по типу
        '''
        return Category.select().where(Category.type == type)

    @classmethod
    def get_by_id(cls, id):
        '''
        Получение категории по ID
        '''
        try:
            return Category.get_by_id(id)
        except Category.DoesNotExist:
            return None

    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление категории
        '''
        try:
            category = Category.get_by_id(id)
            for key, value in kwargs.items():
                if hasattr(category, key) and value is not None:
                    setattr(category, key, value)
            category.save()
            return {'success': True, 'message': f'Категория {category.name} обновлена'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка обновления: {e}'}

    @classmethod
    def delete(cls, id):
        '''
        Удаление категории
        '''
        try:
            category = Category.get_by_id(id)
            name = category.name
            category.delete_instance()
            return {'success': True, 'message': f'Категория {name} удалена'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка удаления: {e}'}