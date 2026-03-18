import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.UserController import UserController


class authView(tk.Tk):
    '''Окно авторизации'''

    def __init__(self):
        super().__init__()

        # Атрибуты окна
        self.title("Авторизация")
        self.geometry("400x450")
        self.resizable(False, False)

        # Центрирование окна
        self.center_window()

        # Фрейм авторизации
        self.auth_user = ttk.Frame(
            self,
            relief=tk.SOLID,
            borderwidth=1,
            padding=[20]
        )
        self.auth_user.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Заголовок
        self.auth_title_frame = ttk.Frame(self.auth_user)
        self.auth_title_frame.pack(fill=tk.X, pady=10)

        self.auth_title = ttk.Label(
            self.auth_title_frame,
            text="HelpDesk",
            font=("Arial", 20, "bold")
        )
        self.auth_title.pack()

        # Фрейм для ввода данных
        self.input_get_user = ttk.Frame(self.auth_user)
        self.input_get_user.pack(fill=tk.X, pady=20)

        # Поля ввода
        ttk.Label(self.input_get_user, text="Логин", font=("Arial", 10)).pack(pady=(10, 5))
        self.login = ttk.Entry(self.input_get_user, width=30, font=("Arial", 10))
        self.login.pack(pady=(0, 10))

        ttk.Label(self.input_get_user, text="Пароль", font=("Arial", 10)).pack(pady=(10, 5))
        self.password = ttk.Entry(self.input_get_user, show='*', width=30, font=("Arial", 10))
        self.password.pack(pady=(0, 10))

        # Кнопка входа
        self.vxod = ttk.Button(
            self.input_get_user,
            text="Войти",
            command=self.auth,
            width=20
        )
        self.vxod.pack(pady=20)

        # Ссылка на регистрацию
        self.reg = tk.Button(
            self.input_get_user,
            text="Нет аккаунта? Зарегистрироваться",
            fg="blue",
            cursor="hand2",
            borderwidth=0,
            font=("Arial", 9),
            command=self.move
        )
        self.reg.pack(pady=5)

        # Привязка Enter
        self.password.bind('<Return>', lambda e: self.auth())

        # Тестовые данные
        test_frame = ttk.LabelFrame(self.auth_user, text="Тестовые данные", padding=10)
        test_frame.pack(fill=tk.X, pady=10)

        ttk.Label(test_frame, text="Админ: admin / admin123").pack(anchor='w')
        ttk.Label(test_frame, text="Специалист: tech / tech123").pack(anchor='w')
        ttk.Label(test_frame, text="Пользователь: user / user123").pack(anchor='w')

    def center_window(self):
        '''Центрирование окна на экране'''
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def auth(self):
        '''Аутентификация пользователя'''
        login = self.login.get()
        password = self.password.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return

        user = UserController.auth(login, password)
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user.full_name or user.login}!")
            self.open_dashboard(user)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def open_dashboard(self, user):
        '''Открытие соответствующей панели в зависимости от роли'''
        from View.Home import HomeView
        self.destroy()
        home = HomeView(user)
        home.mainloop()

    def move(self):
        '''Переход к окну регистрации'''
        from RegistrationView import regView
        self.destroy()
        reg = regView()
        reg.mainloop()


if __name__ == "__main__":
    window = authView()
    window.mainloop()