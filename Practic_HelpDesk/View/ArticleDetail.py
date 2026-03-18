import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.KnowledgeController import KnowledgeController


class ArticleDetailView(tk.Toplevel):
    '''Окно просмотра статьи'''

    def __init__(self, parent, article_id):
        super().__init__(parent)

        self.article = KnowledgeController.get_by_id(article_id)

        if not self.article:
            messagebox.showerror("Ошибка", "Статья не найдена")
            self.destroy()
            return

        self.title(self.article.title)
        self.geometry("600x500")

        # Центрирование окна
        self.center_window()

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        self.setup_ui()

    def center_window(self):
        '''Центрирование окна на экране'''
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self,
            text=self.article.title,
            font=("Arial", 16, "bold"),
            wraplength=550
        )
        title_label.pack(pady=10)

        # Информация
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        category = self.article.category.name if self.article.category else "Без категории"
        author = self.article.created_by.full_name if self.article.created_by else "Неизвестно"

        ttk.Label(
            info_frame,
            text=f"Категория: {category} | Автор: {author} | Просмотров: {self.article.views} | "
                 f"Дата: {self.article.created_at.strftime('%d.%m.%Y')}"
        ).pack()

        # Содержание
        content_frame = ttk.LabelFrame(self, text="Содержание", padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Текстовое поле с прокруткой
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        content_text = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10))
        content_text.insert('1.0', self.article.content)
        content_text.config(state=tk.DISABLED)
        content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=content_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        content_text.configure(yscrollcommand=scrollbar.set)

        # Кнопка закрытия
        ttk.Button(
            self,
            text="Закрыть",
            command=self.destroy
        ).pack(pady=10)