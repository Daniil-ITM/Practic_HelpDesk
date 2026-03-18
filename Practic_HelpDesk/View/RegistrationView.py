import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.UserController import UserController


class regView(tk.Tk):
    '''Окно регистрации'''

    def __init__(self):
        super().__init__()

        # Атрибуты окна
        self.title("Регистрация")
        self.geometry("500x700")
        self.resizable(False, False)

        # Центрирование окна
        self.center_window()

        # Фрейм регистрации
        self.reg_user = ttk.Frame(
            self,
            relief=tk.SOLID,
            borderwidth=1,
            padding=[20]
        )
        self.reg_user.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Заголовок
        self.title_reg = ttk.Frame(self.reg_user)
        self.title_reg.pack(fill=tk.X, pady=10)

        self.reg_title = ttk.Label(
            self.reg_user,
            text="Регистрация",
            font=("Arial", 20, "bold")
        )
        self.reg_title.pack()

        # Фрейм для ввода данных
        self.input_get_user = ttk.Frame(self.reg_user)
        self.input_get_user.pack(fill=tk.X, pady=20)

        # Поля ввода
        ttk.Label(self.input_get_user, text="Логин", font=("Arial", 10)).pack(pady=(10, 5))
        self.login = ttk.Entry(self.input_get_user, width=30, font=("Arial", 10))
        self.login.pack(pady=(0, 10))

        ttk.Label(self.input_get_user, text="Пароль", font=("Arial", 10)).pack(pady=(10, 5))
        self.password = ttk.Entry(self.input_get_user, show='*', width=30, font=("Arial", 10))
        self.password.pack(pady=(0, 10))

        ttk.Label(self.input_get_user, text="Подтверждение пароля", font=("Arial", 10)).pack(pady=(10, 5))
        self.password_confirm = ttk.Entry(self.input_get_user, show='*', width=30, font=("Arial", 10))
        self.password_confirm.pack(pady=(0, 10))

        ttk.Label(self.input_get_user, text="ФИО", font=("Arial", 10)).pack(pady=(10, 5))
        self.full_name = ttk.Entry(self.input_get_user, width=30, font=("Arial", 10))
        self.full_name.pack(pady=(0, 10))

        ttk.Label(self.input_get_user, text="Email", font=("Arial", 10)).pack(pady=(10, 5))
        self.email = ttk.Entry(self.input_get_user, width=30, font=("Arial", 10))
        self.email.pack(pady=(0, 10))

        ttk.Label(self.input_get_user, text="Выберите свою роль", font=("Arial", 10)).pack(pady=(10, 5))
        roles = ['user', 'tech', 'admin']
        role_names = ['Пользователь', 'Специалист', 'Администратор']
        self.role = ttk.Combobox(self.input_get_user, values=role_names, state="readonly", width=27)
        self.role.set('Пользователь')
        self.role.pack(pady=(0, 10))

        # Кнопка регистрации
        self.reg = ttk.Button(
            self.input_get_user,
            text='Зарегистрироваться',
            command=self.add_reg,
            width=20
        )
        self.reg.pack(pady=20)

        # Ссылка на авторизацию
        self.pere = tk.Button(
            self.input_get_user,
            text='Уже есть аккаунт? Войти',
            fg="blue",
            cursor="hand2",
            borderwidth=0,
            font=("Arial", 9),
            command=self.move
        )
        self.pere.pack(pady=5)

    def center_window(self):
        '''Центрирование окна на экране'''
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def move(self):
        '''Переход к окну авторизации'''
        from View.AuthView import authView
        self.destroy()
        auth = authView()
        auth.mainloop()

    def add_reg(self):
        '''Регистрация нового пользователя'''
        login = self.login.get()
        password = self.password.get()
        password_confirm = self.password_confirm.get()
        full_name = self.full_name.get()
        email = self.email.get()
        role_name = self.role.get()

        # Валидация
        if not login or not password or not full_name:
            messagebox.showerror("Ошибка", "Заполните все обязательные поля")
            return

        if password != password_confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        # Преобразование роли
        role_map = {'Пользователь': 'user', 'Специалист': 'tech', 'Администратор': 'admin'}
        role = role_map.get(role_name, 'user')

        # Регистрация
        result = UserController.registration(login, password, full_name, email, role)

        if result['success']:
            messagebox.showinfo("Успех", result['message'])
            self.move()
        else:
            messagebox.showerror("Ошибка", result['message'])