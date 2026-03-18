import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.TicketsController import TicketController
from Controllers.CommentsController import CommentController
from Controllers.UserController import UserController


class TicketDetailView(tk.Toplevel):
    '''Окно просмотра заявки'''

    def __init__(self, parent, ticket_id, user, on_update):
        super().__init__(parent)

        self.ticket_id = ticket_id
        self.user = user
        self.on_update = on_update

        self.title(f"Заявка №{ticket_id}")
        self.geometry("600x600")

        # Загрузка заявки
        self.ticket = TicketController.get_by_id(ticket_id)

        # Центрирование окна
        self.center_window()

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        if self.ticket:
            self.setup_ui()
            self.load_comments()
        else:
            messagebox.showerror("Ошибка", "Заявка не найдена")
            self.destroy()

    def center_window(self):
        '''Центрирование окна на экране'''
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        status_names = {
            'new': 'Новая',
            'in_progress': 'В работе',
            'resolved': 'Решена',
            'closed': 'Закрыта'
        }

        # Основная информация
        main_frame = ttk.LabelFrame(self, text="Информация о заявке", padding=10)
        main_frame.pack(fill=tk.X, padx=10, pady=5)

        info_text = f"""
№ заявки: {self.ticket.id}
Тема: {self.ticket.title}
Статус: {status_names.get(self.ticket.status, self.ticket.status)}
Создатель: {self.ticket.created_by.full_name if self.ticket.created_by else "Неизвестно"}
Дата создания: {self.ticket.created_at.strftime('%d.%m.%Y %H:%M')}
Назначена: {self.ticket.assigned_to.full_name if self.ticket.assigned_to else "Не назначена"}
Категория: {self.ticket.category.name if self.ticket.category else "Без категории"}
        """

        tk.Label(main_frame, text=info_text, justify=tk.LEFT).pack(anchor='w')

        # Описание
        desc_frame = ttk.LabelFrame(self, text="Описание", padding=10)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        desc_text = tk.Text(desc_frame, height=5, wrap=tk.WORD)
        desc_text.insert('1.0', self.ticket.description)
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.X)

        # Комментарии
        comments_frame = ttk.LabelFrame(self, text="Комментарии", padding=10)
        comments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Список комментариев
        self.comments_list = tk.Text(comments_frame, height=8, wrap=tk.WORD)
        self.comments_list.config(state=tk.DISABLED)
        self.comments_list.pack(fill=tk.BOTH, expand=True)

        # Новый комментарий
        new_comment_frame = ttk.Frame(self)
        new_comment_frame.pack(fill=tk.X, padx=10, pady=5)

        self.comment_entry = ttk.Entry(new_comment_frame, width=50)
        self.comment_entry.pack(side=tk.LEFT, padx=5)

        # Чекбокс для приватного комментария
        self.private_var = tk.BooleanVar()
        if self.user.role in ['admin', 'tech']:
            ttk.Checkbutton(
                new_comment_frame,
                text="Приватный",
                variable=self.private_var
            ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            new_comment_frame,
            text="Отправить",
            command=self.add_comment
        ).pack(side=tk.LEFT, padx=5)

        # Кнопки изменения статуса
        if self.user.role in ['admin', 'tech']:
            status_frame = ttk.Frame(self)
            status_frame.pack(fill=tk.X, padx=10, pady=5)

            ttk.Label(status_frame, text="Изменить статус:").pack(side=tk.LEFT)

            status_buttons = [
                ('new', 'Новая'),
                ('in_progress', 'В работе'),
                ('resolved', 'Решена'),
                ('closed', 'Закрыта')
            ]

            for status, display in status_buttons:
                btn = ttk.Button(
                    status_frame,
                    text=display,
                    command=lambda s=status: self.change_status(s)
                )
                btn.pack(side=tk.LEFT, padx=2)

            # Кнопка назначения специалиста
            if self.user.role == 'admin':
                ttk.Button(
                    status_frame,
                    text="Назначить специалиста",
                    command=self.assign_tech
                ).pack(side=tk.LEFT, padx=20)

    def load_comments(self):
        '''Загрузка комментариев'''
        comments = CommentController.get_by_ticket(self.ticket_id, self.user)

        self.comments_list.config(state=tk.NORMAL)
        self.comments_list.delete('1.0', tk.END)

        for comment in comments:
            private_tag = "[ПРИВАТНЫЙ] " if comment.is_private else ""
            self.comments_list.insert(tk.END,
                                      f"{private_tag}{comment.user.full_name or comment.user.login} "
                                      f"({comment.created_at.strftime('%d.%m.%Y %H:%M')}):\n"
                                      )
            self.comments_list.insert(tk.END, f"{comment.content}\n")
            self.comments_list.insert(tk.END, "-" * 50 + "\n")

        self.comments_list.config(state=tk.DISABLED)
        self.comments_list.see(tk.END)

    def add_comment(self):
        '''Добавление комментария'''
        content = self.comment_entry.get().strip()
        if not content:
            return

        result = CommentController.create(
            content,
            self.user.id,
            self.ticket_id,
            self.private_var.get()
        )

        if result['success']:
            self.comment_entry.delete(0, tk.END)
            self.private_var.set(False)
            self.load_comments()
        else:
            messagebox.showerror("Ошибка", result['message'])

    def change_status(self, new_status):
        '''Изменение статуса заявки'''
        result = TicketController.update_status(self.ticket_id, new_status)

        if result['success']:
            messagebox.showinfo("Успех", result['message'])
            self.ticket = TicketController.get_by_id(self.ticket_id)
            self.on_update()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", result['message'])

    def assign_tech(self):
        '''Назначение специалиста'''
        from View.SelectTech import SelectTechView
        SelectTechView(self, self.ticket_id, self.on_tech_assigned)

    def on_tech_assigned(self):
        '''Обработчик назначения специалиста'''
        self.ticket = TicketController.get_by_id(self.ticket_id)
        self.on_update()
        self.destroy()