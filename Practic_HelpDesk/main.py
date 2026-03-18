#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Главный файл запуска приложения HelpDesk
Система технической поддержки
"""

import sys
import os
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

import tkinter as tk
from tkinter import messagebox

# Импорты модулей проекта
from Connection.connect import connect
from Models.create_table import create_tables
from View.AuthView import authView


def check_database():
    """
    Проверка наличия таблиц в базе данных
    Если таблиц нет - создаем их
    """
    print("=" * 50)
    print(" Запуск системы технической поддержки HelpDesk")
    print("=" * 50)

    try:
        # Подключаемся к БД
        db = connect()

        if not db:
            print(" Не удалось подключиться к базе данных")
            return False

        # Проверяем наличие таблиц
        tables = ['users', 'categories', 'tickets', 'comments', 'knowledge_base', 'knowledge_faq']
        existing_tables = db.get_tables()

        # Если таблиц нет или их меньше необходимого, создаем их
        if not all(table in existing_tables for table in tables):
            print(" Таблицы не найдены или неполные, инициализация базы данных...")
            db.close()
            return create_tables()

        db.close()
        print(" База данных готова к работе")
        return True

    except Exception as e:
        print(f" Ошибка проверки базы данных: {e}")
        return False


def main():
    """
    Главная функция запуска приложения
    """
    # Проверяем базу данных перед запуском
    if not check_database():
        print("\n Критическая ошибка: не удалось инициализировать базу данных")
        print("Пожалуйста, проверьте:")
        print("  1. Запущен ли MySQL сервер")
        print("  2. Правильность настроек подключения в Connection/connect.py")
        print("  3. Доступность базы данных")

        # Показываем сообщение об ошибке в GUI
        root = tk.Tk()
        root.withdraw()  # Скрываем главное окно
        messagebox.showerror(
            "Критическая ошибка",
            "Не удалось подключиться к базе данных!\n\n"
            "Пожалуйста, проверьте:\n"
            "• Запущен ли MySQL сервер\n"
            "• Правильность настроек подключения\n"
            "• Доступность базы данных"
        )
        root.destroy()
        sys.exit(1)

    print("\n Запуск графического интерфейса...")

    # Запускаем приложение
    try:
        app = authView()
        app.mainloop()
    except Exception as e:
        print(f" Ошибка при запуске приложения: {e}")

        # Показываем сообщение об ошибке
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Ошибка запуска",
            f"Произошла ошибка при запуске приложения:\n\n{e}"
        )
        root.destroy()
        sys.exit(1)

    print("\n👋 Приложение завершено")


if __name__ == "__main__":
    main()