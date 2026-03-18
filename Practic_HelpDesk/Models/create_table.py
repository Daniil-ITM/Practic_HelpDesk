import os
import sys
from pathlib import Path



# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent.parent))

from Connection.connect import connect
from Models.Users import User
from Models.Categories import Category
from Models.Tickets import Ticket
from Models.Comments import Comment
from Models.Knowledgebase import KnowledgeBase
import datetime
from Controllers.UserController import UserController


def create_tables():
    """Создание всех таблиц в базе данных"""
    print("=" * 50)
    print(" Инициализация базы данных")
    print("=" * 50)

    db = connect()

    if not db:
        print(" Не удалось подключиться к базе данных")
        return False

    try:
        print("\n Создание таблиц...")
        db.create_tables([
            User,
            Category,
            Ticket,
            Comment,
            KnowledgeBase
        ], safe=True)
        print(" Таблицы успешно созданы!")

        # Создание тестовых пользователей
        if User.select().count() == 0:
            print("\n Создание тестовых пользователей...")

            # Админ
            admin = User.create(
                login='admin',
                password_hash=UserController.hash_password('admin123'),
                role='admin',
                full_name='Администратор Системы',
                email='admin@example.com'
            )
            print(f"  - Создан: admin (администратор)")

            # Специалист
            tech = User.create(
                login='tech',
                password_hash=UserController.hash_password('tech123'),
                role='tech',
                full_name='Иванов Иван (Специалист)',
                email='tech@example.com'
            )
            print(f"  - Создан: tech (специалист)")

            # Пользователь
            user = User.create(
                login='user',
                password_hash=UserController.hash_password('user123'),
                role='user',
                full_name='Петров Петр',
                email='user@example.com'
            )
            print(f"  - Создан: user (пользователь)")

        # Создание категорий
        if Category.select().count() == 0:
            print("\n Создание категорий...")
            categories = [
                {'name': 'Проблемы с ПК', 'type': 'ticket', 'description': 'Аппаратные проблемы'},
                {'name': 'Программное обеспечение', 'type': 'ticket', 'description': 'Проблемы с ПО'},
                {'name': 'Сетевые проблемы', 'type': 'ticket', 'description': 'Проблемы с сетью'},
                {'name': 'Другое', 'type': 'ticket', 'description': 'Прочие проблемы'},
                {'name': 'Инструкции', 'type': 'article', 'description': 'Полезные инструкции'},
                {'name': 'FAQ', 'type': 'article', 'description': 'Часто задаваемые вопросы'},
            ]

            for cat in categories:
                Category.create(**cat)
                print(f"  - Создана: {cat['name']}")

        print("\n" + "=" * 50)
        print(" База данных успешно инициализирована!")
        print("=" * 50)
        print("\n Тестовые учетные записи:")
        print("   Админ: admin / admin123")
        print("   Специалист: tech / tech123")
        print("   Пользователь: user / user123")

        return True

    except Exception as e:
        print(f"\n Ошибка при создании таблиц: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()