from Models.Knowledgebase import KnowledgeBase
from Models.Users import User
from Models.Categories import Category


class KnowledgeController:
    '''
    Класс для работы с базой знаний
    '''

    @classmethod
    def create(cls, title, content, created_by_id, category_id=None):
        '''
        Создание статьи
        '''
        try:
            created_by = User.get_by_id(created_by_id)
            category = Category.get_by_id(category_id) if category_id else None

            article = KnowledgeBase.create(
                title=title,
                content=content,
                category=category,
                created_by=created_by
            )
            return {'success': True, 'message': f'Статья "{title}" создана', 'article': article}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка создания статьи: {e}'}

    @classmethod
    def get(cls):
        '''
        Получение всех статей
        '''
        return KnowledgeBase.select().order_by(KnowledgeBase.created_at.desc())

    @classmethod
    def get_by_id(cls, id):
        '''
        Получение статьи по ID с увеличением просмотров
        '''
        try:
            article = KnowledgeBase.get_by_id(id)
            article.views = (article.views or 0) + 1
            article.save()
            return article
        except KnowledgeBase.DoesNotExist:
            return None

    @classmethod
    def get_by_category(cls, category_id):
        '''
        Получение статей по категории
        '''
        return KnowledgeBase.select().where(
            KnowledgeBase.category == category_id
        ).order_by(KnowledgeBase.created_at.desc())

    @classmethod
    def search(cls, query):
        '''
        Поиск статей
        '''
        return KnowledgeBase.select().where(
            (KnowledgeBase.title.contains(query)) |
            (KnowledgeBase.content.contains(query))
        ).order_by(KnowledgeBase.created_at.desc())

    @classmethod
    def get_popular(cls, limit=5):
        '''
        Получение популярных статей
        '''
        return KnowledgeBase.select().order_by(KnowledgeBase.views.desc()).limit(limit)

    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление статьи
        '''
        try:
            article = KnowledgeBase.get_by_id(id)
            for key, value in kwargs.items():
                if hasattr(article, key) and value is not None:
                    setattr(article, key, value)
            article.save()
            return {'success': True, 'message': f'Статья "{article.title}" обновлена'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка обновления: {e}'}

    @classmethod
    def delete(cls, id):
        '''
        Удаление статьи
        '''
        try:
            article = KnowledgeBase.get_by_id(id)
            title = article.title
            article.delete_instance()
            return {'success': True, 'message': f'Статья "{title}" удалена'}
        except Exception as e:
            return {'success': False, 'message': f'Ошибка удаления: {e}'}