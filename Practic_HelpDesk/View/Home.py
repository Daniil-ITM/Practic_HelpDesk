import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.TicketsController import TicketController

from Controllers.AnalyticsController import AnalyticsController
from Controllers.KnowledgeController import KnowledgeController
from Controllers.CategoryController import CategoryController
from Models.Categories import Category

class HomeView(tk.Tk):
    '''Главное окно'''

    def __init__(self, user):
        super().__init__()

        self.user = user

        # Атрибуты окна
        self.title(f"HelpDesk - {user.full_name or user.login} ({user.role})")
        self.geometry("1000x700")

        # Центрирование окна
        self.center_window()

        # Главный фрейм
        self.home = ttk.Frame(
            self,
            relief=tk.SOLID,
            borderwidth=1,
            padding=[10]
        )
        self.home.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель
        self.top_frame = ttk.Frame(self.home)
        self.top_frame.pack(fill=tk.X, pady=5)

        ttk.Label(
            self.top_frame,
            text=f"Пользователь: {user.full_name or user.login}",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)

        ttk.Button(
            self.top_frame,
            text="Выход",
            command=self.logout
        ).pack(side=tk.RIGHT)

        # Ноутбук для вкладок
        self.notebook = ttk.Notebook(self.home)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Вкладка "Мои заявки"
        self.tickets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tickets_frame, text="Мои заявки")
        self.setup_tickets_tab()

        # Вкладка "База знаний"
        self.knowledge_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.knowledge_frame, text="База знаний")
        self.setup_knowledge_tab()

        # Для админов и специалистов добавляем вкладку "Все заявки"
        if user.role in ['admin', 'tech']:
            self.all_tickets_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.all_tickets_frame, text="Все заявки")
            self.setup_all_tickets_tab()

            # Вкладка аналитики
            self.analytics_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.analytics_frame, text="Аналитика")
            self.setup_analytics_tab()

        # Загрузка данных
        self.load_tickets()
        self.load_knowledge()
        if user.role in ['admin', 'tech']:
            self.load_all_tickets()
            self.load_analytics()

    def center_window(self):
        '''Центрирование окна на экране'''
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_tickets_tab(self):
        '''Настройка вкладки "Мои заявки"'''

        # Кнопка создания заявки
        create_btn = ttk.Button(
            self.tickets_frame,
            text="+ Создать новую заявку",
            command=self.open_create_ticket
        )
        create_btn.pack(pady=10)

        # Панель поиска и фильтрации
        control_frame = ttk.Frame(self.tickets_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_tickets())

        ttk.Label(control_frame, text="Статус:").pack(side=tk.LEFT, padx=(20, 5))
        self.status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(
            control_frame,
            textvariable=self.status_var,
            values=["all", "new", "in_progress", "resolved", "closed"],
            width=15,
            state="readonly"
        )
        status_combo.pack(side=tk.LEFT)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_tickets())

        # Таблица заявок
        columns = ('id', 'title', 'status', 'created_at', 'assigned_to')
        self.tree = ttk.Treeview(self.tickets_frame, columns=columns, show='headings', height=15)

        self.tree.heading('id', text='№ заявки')
        self.tree.heading('title', text='Тема')
        self.tree.heading('status', text='Статус')
        self.tree.heading('created_at', text='Дата создания')
        self.tree.heading('assigned_to', text='Назначена')

        self.tree.column('id', width=80)
        self.tree.column('title', width=300)
        self.tree.column('status', width=100)
        self.tree.column('created_at', width=150)
        self.tree.column('assigned_to', width=150)

        # Скроллбар
        scrollbar = ttk.Scrollbar(self.tickets_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Двойной клик по заявке
        self.tree.bind('<Double-1>', lambda e: self.open_ticket_detail())

    def setup_all_tickets_tab(self):
        '''Настройка вкладки "Все заявки"'''

        # Панель поиска и фильтрации
        control_frame = ttk.Frame(self.all_tickets_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Поиск:").pack(side=tk.LEFT)
        self.all_search_entry = ttk.Entry(control_frame, width=30)
        self.all_search_entry.pack(side=tk.LEFT, padx=5)
        self.all_search_entry.bind('<KeyRelease>', lambda e: self.search_all_tickets())

        ttk.Label(control_frame, text="Статус:").pack(side=tk.LEFT, padx=(20, 5))
        self.all_status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(
            control_frame,
            textvariable=self.all_status_var,
            values=["all", "new", "in_progress", "resolved", "closed"],
            width=15,
            state="readonly"
        )
        status_combo.pack(side=tk.LEFT)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_all_tickets())

        # Таблица всех заявок
        columns = ('id', 'title', 'status', 'created_by', 'assigned_to', 'created_at')
        self.all_tree = ttk.Treeview(self.all_tickets_frame, columns=columns, show='headings', height=15)

        self.all_tree.heading('id', text='№ заявки')
        self.all_tree.heading('title', text='Тема')
        self.all_tree.heading('status', text='Статус')
        self.all_tree.heading('created_by', text='Создатель')
        self.all_tree.heading('assigned_to', text='Назначена')
        self.all_tree.heading('created_at', text='Дата')

        self.all_tree.column('id', width=80)
        self.all_tree.column('title', width=250)
        self.all_tree.column('status', width=100)
        self.all_tree.column('created_by', width=150)
        self.all_tree.column('assigned_to', width=150)
        self.all_tree.column('created_at', width=150)

        # Скроллбар
        scrollbar = ttk.Scrollbar(self.all_tickets_frame, orient=tk.VERTICAL, command=self.all_tree.yview)
        self.all_tree.configure(yscrollcommand=scrollbar.set)

        self.all_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Двойной клик по заявке
        self.all_tree.bind('<Double-1>', lambda e: self.open_ticket_detail(True))

    def setup_knowledge_tab(self):
        '''Настройка вкладки "База знаний"'''

        # Панель поиска
        search_frame = ttk.Frame(self.knowledge_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.kb_search_entry = ttk.Entry(search_frame, width=40)
        self.kb_search_entry.pack(side=tk.LEFT, padx=5)
        self.kb_search_entry.bind('<KeyRelease>', lambda e: self.search_articles())

        # Для админов и специалистов - кнопка создания статьи
        if self.user.role in ['admin', 'tech']:
            ttk.Button(
                search_frame,
                text="+ Новая статья",
                command=self.open_create_article
            ).pack(side=tk.RIGHT, padx=5)

        # Список категорий
        categories_frame = ttk.Frame(self.knowledge_frame)
        categories_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(categories_frame, text="Категории:").pack(side=tk.LEFT)
        categories = CategoryController.get_by_type('article')
        category_names = ['Все'] + [cat.name for cat in categories]

        self.category_var = tk.StringVar(value="Все")
        category_combo = ttk.Combobox(
            categories_frame,
            textvariable=self.category_var,
            values=category_names,
            width=20,
            state="readonly"
        )
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_articles())

        # Таблица статей
        columns = ('title', 'category', 'views', 'created_by', 'created_at')
        self.kb_tree = ttk.Treeview(self.knowledge_frame, columns=columns, show='headings', height=15)

        self.kb_tree.heading('title', text='Название статьи')
        self.kb_tree.heading('category', text='Категория')
        self.kb_tree.heading('views', text='Просмотры')
        self.kb_tree.heading('created_by', text='Автор')
        self.kb_tree.heading('created_at', text='Дата')

        self.kb_tree.column('title', width=300)
        self.kb_tree.column('category', width=150)
        self.kb_tree.column('views', width=80)
        self.kb_tree.column('created_by', width=150)
        self.kb_tree.column('created_at', width=150)

        # Скроллбар
        kb_scrollbar = ttk.Scrollbar(self.knowledge_frame, orient=tk.VERTICAL, command=self.kb_tree.yview)
        self.kb_tree.configure(yscrollcommand=kb_scrollbar.set)

        self.kb_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        kb_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Двойной клик по статье
        self.kb_tree.bind('<Double-1>', lambda e: self.open_article())

    def setup_analytics_tab(self):
        '''Настройка вкладки аналитики'''

        # Статистика по статусам
        stats_frame = ttk.LabelFrame(self.analytics_frame, text="Статистика заявок", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        self.stats_text = tk.Text(stats_frame, height=8, width=50)
        self.stats_text.pack()

    def load_tickets(self):
        '''Загрузка заявок пользователя'''
        for row in self.tree.get_children():
            self.tree.delete(row)

        tickets = TicketController.get_by_user(self.user.id)

        status_names = {
            'new': 'Новая',
            'in_progress': 'В работе',
            'resolved': 'Решена',
            'closed': 'Закрыта'
        }

        for ticket in tickets:
            assigned = ticket.assigned_to.full_name if ticket.assigned_to else "Не назначена"
            self.tree.insert('', tk.END, values=(
                ticket.id,
                ticket.title,
                status_names.get(ticket.status, ticket.status),
                ticket.created_at.strftime("%d.%m.%Y %H:%M"),
                assigned
            ), tags=(ticket.id,))

    def load_all_tickets(self):
        '''Загрузка всех заявок'''
        if not hasattr(self, 'all_tree'):
            return

        for row in self.all_tree.get_children():
            self.all_tree.delete(row)

        tickets = TicketController.get()

        status_names = {
            'new': 'Новая',
            'in_progress': 'В работе',
            'resolved': 'Решена',
            'closed': 'Закрыта'
        }

        for ticket in tickets:
            created_by = ticket.created_by.full_name if ticket.created_by else "Неизвестно"
            assigned = ticket.assigned_to.full_name if ticket.assigned_to else "Не назначена"
            self.all_tree.insert('', tk.END, values=(
                ticket.id,
                ticket.title,
                status_names.get(ticket.status, ticket.status),
                created_by,
                assigned,
                ticket.created_at.strftime("%d.%m.%Y %H:%M")
            ), tags=(ticket.id,))

    def load_knowledge(self):
        '''Загрузка статей базы знаний'''
        for row in self.kb_tree.get_children():
            self.kb_tree.delete(row)

        articles = KnowledgeController.get()

        for article in articles:
            category = article.category.name if article.category else "Без категории"
            author = article.created_by.full_name if article.created_by else "Неизвестно"
            self.kb_tree.insert('', tk.END, values=(
                article.title,
                category,
                article.views,
                author,
                article.created_at.strftime("%d.%m.%Y")
            ), tags=(article.id,))

    def load_analytics(self):
        '''Загрузка аналитики'''
        stats = AnalyticsController.get_tickets_by_status()

        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', "Количество заявок по статусам:\n\n")
        for status, count in stats.items():
            self.stats_text.insert(tk.END, f"{status}: {count}\n")
        self.stats_text.config(state=tk.DISABLED)

    def search_tickets(self):
        '''Поиск по заявкам пользователя'''
        query = self.search_entry.get()
        if query:
            for row in self.tree.get_children():
                self.tree.delete(row)

            tickets = TicketController.search(query)
            tickets = [t for t in tickets if t.created_by.id == self.user.id]

            status_names = {
                'new': 'Новая',
                'in_progress': 'В работе',
                'resolved': 'Решена',
                'closed': 'Закрыта'
            }

            for ticket in tickets:
                assigned = ticket.assigned_to.full_name if ticket.assigned_to else "Не назначена"
                self.tree.insert('', tk.END, values=(
                    ticket.id,
                    ticket.title,
                    status_names.get(ticket.status, ticket.status),
                    ticket.created_at.strftime("%d.%m.%Y %H:%M"),
                    assigned
                ), tags=(ticket.id,))
        else:
            self.load_tickets()

    def search_all_tickets(self):
        '''Поиск по всем заявкам'''
        if not hasattr(self, 'all_tree'):
            return

        query = self.all_search_entry.get()
        if query:
            for row in self.all_tree.get_children():
                self.all_tree.delete(row)

            tickets = TicketController.search(query)

            status_names = {
                'new': 'Новая',
                'in_progress': 'В работе',
                'resolved': 'Решена',
                'closed': 'Закрыта'
            }

            for ticket in tickets:
                created_by = ticket.created_by.full_name if ticket.created_by else "Неизвестно"
                assigned = ticket.assigned_to.full_name if ticket.assigned_to else "Не назначена"
                self.all_tree.insert('', tk.END, values=(
                    ticket.id,
                    ticket.title,
                    status_names.get(ticket.status, ticket.status),
                    created_by,
                    assigned,
                    ticket.created_at.strftime("%d.%m.%Y %H:%M")
                ), tags=(ticket.id,))
        else:
            self.load_all_tickets()

    def filter_tickets(self):
        '''Фильтрация заявок по статусу'''
        status = self.status_var.get()
        if status != "all":
            for row in self.tree.get_children():
                self.tree.delete(row)

            tickets = TicketController.get_by_status(status)
            tickets = [t for t in tickets if t.created_by.id == self.user.id]

            status_names = {
                'new': 'Новая',
                'in_progress': 'В работе',
                'resolved': 'Решена',
                'closed': 'Закрыта'
            }

            for ticket in tickets:
                assigned = ticket.assigned_to.full_name if ticket.assigned_to else "Не назначена"
                self.tree.insert('', tk.END, values=(
                    ticket.id,
                    ticket.title,
                    status_names.get(ticket.status, ticket.status),
                    ticket.created_at.strftime("%d.%m.%Y %H:%M"),
                    assigned
                ), tags=(ticket.id,))
        else:
            self.load_tickets()

    def filter_all_tickets(self):
        '''Фильтрация всех заявок по статусу'''
        if not hasattr(self, 'all_tree'):
            return

        status = self.all_status_var.get()
        if status != "all":
            for row in self.all_tree.get_children():
                self.all_tree.delete(row)

            tickets = TicketController.get_by_status(status)

            status_names = {
                'new': 'Новая',
                'in_progress': 'В работе',
                'resolved': 'Решена',
                'closed': 'Закрыта'
            }

            for ticket in tickets:
                created_by = ticket.created_by.full_name if ticket.created_by else "Неизвестно"
                assigned = ticket.assigned_to.full_name if ticket.assigned_to else "Не назначена"
                self.all_tree.insert('', tk.END, values=(
                    ticket.id,
                    ticket.title,
                    status_names.get(ticket.status, ticket.status),
                    created_by,
                    assigned,
                    ticket.created_at.strftime("%d.%m.%Y %H:%M")
                ), tags=(ticket.id,))
        else:
            self.load_all_tickets()

    def search_articles(self):
        '''Поиск статей'''
        query = self.kb_search_entry.get()
        if query:
            for row in self.kb_tree.get_children():
                self.kb_tree.delete(row)

            articles = KnowledgeController.search(query)

            for article in articles:
                category = article.category.name if article.category else "Без категории"
                author = article.created_by.full_name if article.created_by else "Неизвестно"
                self.kb_tree.insert('', tk.END, values=(
                    article.title,
                    category,
                    article.views,
                    author,
                    article.created_at.strftime("%d.%m.%Y")
                ), tags=(article.id,))
        else:
            self.load_knowledge()

    def filter_articles(self):
        '''Фильтрация статей по категории'''
        category_name = self.category_var.get()
        if category_name != "Все":
            for row in self.kb_tree.get_children():
                self.kb_tree.delete(row)

            category = CategoryController.get_by_type('article').where(Category.name == category_name).first()
            if category:
                articles = KnowledgeController.get_by_category(category.id)

                for article in articles:
                    author = article.created_by.full_name if article.created_by else "Неизвестно"
                    self.kb_tree.insert('', tk.END, values=(
                        article.title,
                        category_name,
                        article.views,
                        author,
                        article.created_at.strftime("%d.%m.%Y")
                    ), tags=(article.id,))
        else:
            self.load_knowledge()

    def open_create_ticket(self):
        '''Открытие окна создания заявки'''
        from View.Createticketwindow import CreateTicketView
        CreateTicketView(self, self.user.id, self.on_ticket_created)

    def open_create_article(self):
        '''Открытие окна создания статьи'''
        from View.CreateArticle import CreateArticleView
        CreateArticleView(self, self.user.id, self.on_article_created)

    def open_ticket_detail(self, all_tickets=False):
        '''Открытие окна деталей заявки '''
        tree = self.all_tree if all_tickets else self.tree
        selected = tree.selection()
        if selected:
            ticket_id = tree.item(selected[0])['tags'][0]
            from View.Ticketdetailwindow import TicketDetailView
            TicketDetailView(self, ticket_id, self.user, self.on_ticket_updated)

    def open_article(self):
        '''Открытие статьи'''
        selected = self.kb_tree.selection()
        if selected:
            article_id = self.kb_tree.item(selected[0])['tags'][0]
            from View.ArticleDetail import ArticleDetailView
            ArticleDetailView(self, article_id)

    def on_ticket_created(self):
        '''Обработчик создания заявки'''
        self.load_tickets()
        if hasattr(self, 'all_tree'):
            self.load_all_tickets()
        self.notebook.select(0)

    def on_ticket_updated(self):
        '''Обработчик обновления заявки'''
        self.load_tickets()
        if hasattr(self, 'all_tree'):
            self.load_all_tickets()

    def on_article_created(self):
        '''Обработчик создания статьи'''
        self.load_knowledge()
        self.notebook.select(1)

    def logout(self):
        '''Выход из системы'''
        from View.AuthView import authView
        self.destroy()
        auth = authView()
        auth.mainloop()