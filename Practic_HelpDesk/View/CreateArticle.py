import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.KnowledgeController import KnowledgeController
from Controllers.CategoryController import CategoryController
from Models.Categories import Category

class CreateArticleView(tk.Toplevel):
    '''Окно создания статьи'''

    def __init__(self, parent, user_id, on_success):
        super().__init__(parent)

        self.user_id = user_id
        self.on_success = on_success

        self.title("Создание статьи")
        self.geometry("500x450")
        self.resizable(False, False)

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
            text="Создание статьи",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Форма
        form_frame = ttk.Frame(self, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок статьи
        ttk.Label(form_frame, text="Заголовок:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = ttk.Entry(form_frame, width=40, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, pady=5)

        # Категория
        ttk.Label(form_frame, text="Категория:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        categories = CategoryController.get_by_type('article')
        category_names = [cat.name for cat in categories]

        self.category_combo = ttk.Combobox(
            form_frame,
            values=category_names,
            width=37,
            state="readonly",
            font=("Arial", 10)
        )
        self.category_combo.grid(row=1, column=1, pady=5)

        # Содержание
        ttk.Label(form_frame, text="Содержание:", font=("Arial", 10)).grid(row=2, column=0, sticky='nw', pady=5)

        # Текстовое поле с прокруткой
        text_frame = ttk.Frame(form_frame)
        text_frame.grid(row=2, column=1, pady=5)

        self.content_text = tk.Text(text_frame, width=40, height=10, font=("Arial", 10))
        self.content_text.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.content_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.configure(yscrollcommand=scrollbar.set)

        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(
            button_frame,
            text="Создать",
            command=self.create_article
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def create_article(self):
        '''Создание статьи'''
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        category_name = self.category_combo.get()

        if not title:
            messagebox.showerror("Ошибка", "Введите заголовок статьи")
            return

        if not content:
            messagebox.showerror("Ошибка", "Введите содержание статьи")
            return

        # Получаем ID категории
        category_id = None
        if category_name:
            category = CategoryController.get_by_type('article').where(Category.name == category_name).first()
            if category:
                category_id = category.id

        # Создаем статью
        result = KnowledgeController.create(title, content, self.user_id, category_id)

        if result['success']:
            messagebox.showinfo("Успех", result['message'])
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", result['message'])