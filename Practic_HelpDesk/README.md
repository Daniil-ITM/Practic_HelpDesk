# Информационная система «Техническая поддержка»
## Наименование проекта
Полное наименование: **Информационная система «Техническая поддержка» (HelpDesk).**  
Краткое наименование: **ИС «TechSupport».**

---
### Структура проекта
```
HelpDesk/
|-- Connection/
|   |-- connect.py
|-- Controller/
|   |-- AnalyticsController.py
|   |-- CategoryController.py
|   |-- CommentsController.py
|   |-- KnowledgeController.py
|   |-- TicketsController.py
|   |-- UserController.py
|-- Models/
|   |-- Base.py
|   |-- Categories.py
|   |-- Comments.py
|   |-- create_table.py
|   |-- Knowledgebase.py
|   |-- Tickets.py
|   |-- Users.py
|-- View/
    |ArticleDetail.py
    |AuthView.py
    |CreateArticle.py
    |Home.py
    |Registration.py
    |SelectTech.py
    |Ticketdetailwindow.py
|-- main.py
|-- library.txt
```

---
### Технологии
- **Python**
- **Tkinter**
- **Peewee**
- **MySQL**
- **PyMySQL**


---
## Установка
1. Установить зависимости:
```bash
pip install -r library.txt
```
2. Настроить подключение к локальной БД в `Connection/connect.py`.
3. Создать таблицы в БД:
```bash
python Models/create_table.py
```
4. Запуск приложения:
```bash
python main.py
