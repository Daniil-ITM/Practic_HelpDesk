from peewee import *
import pymysql

def connect():
    """Подключение к базе данных MySQL"""
    try:
        database = MySQLDatabase(
            'practic_help',
            user='root',
            password='',
            host='127.0.0.1',
            port=3306
        )
        return database
    except Exception as e:
        print(f'Ошибка подключения к БД: {e}')
        return None

if __name__ == "__main__":
    db = connect()
    if db:
        print(db.connect())