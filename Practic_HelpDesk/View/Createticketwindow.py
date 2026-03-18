import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.TicketsController import TicketController
from Controllers.CategoryController import CategoryController
from Models.Categories import Category


class CreateTicketView(tk.Toplevel):
    '''Окно создания заявки'''

    def __init__(self, parent, user_id, on_success):
        super().__init__(parent)

        self.user_id = user_id
        self.on_success = on_success

        self.title("Создание заявки")
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
            text="Создать заявку",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Форма
        form_frame = ttk.Frame(self, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Тема
        ttk.Label(form_frame, text="Тема:", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = ttk.Entry(form_frame, width=40, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, pady=5)

        # Категория
        ttk.Label(form_frame, text="Категория:", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        categories = CategoryController.get_by_type('ticket')
        category_names = [cat.name for cat in categories]

        self.category_combo = ttk.Combobox(
            form_frame,
            values=category_names,
            width=37,
            state="readonly",
            font=("Arial", 10)
        )
        self.category_combo.grid(row=1, column=1, pady=5)
        if category_names:
            self.category_combo.set(category_names[0])

        # Описание
        ttk.Label(form_frame, text="Описание:", font=("Arial", 10)).grid(row=2, column=0, sticky='nw', pady=5)

        # Текстовое поле с прокруткой
        text_frame = ttk.Frame(form_frame)
        text_frame.grid(row=2, column=1, pady=5)

        self.description_text = tk.Text(text_frame, width=40, height=10, font=("Arial", 10))
        self.description_text.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.description_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.description_text.configure(yscrollcommand=scrollbar.set)

        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(
            button_frame,
            text="Прикрепить файл",
            command=self.attach_file
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Отправить",
            command=self.create_ticket
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def attach_file(self):
        '''Прикрепление файла'''
        messagebox.showinfo("Информация", "Функция прикрепления файлов будет добавлена позже")

    def create_ticket(self):
        '''Создание заявки'''
        title = self.title_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()
        category_name = self.category_combo.get()

        if not title:
            messagebox.showerror("Ошибка", "Введите тему заявки")
            return

        if not description:
            messagebox.showerror("Ошибка", "Введите описание заявки")
            return

        # Получаем ID категории
        category_id = None
        if category_name:
            category = CategoryController.get_by_type('ticket').where(Category.name == category_name).first()
            if category:
                category_id = category.id

        # Создаем заявку
        result = TicketController.create(title, description, self.user_id, category_id)

        if result['success']:
            messagebox.showinfo("Успех", result['message'])
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", result['message'])