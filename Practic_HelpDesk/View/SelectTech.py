import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.UserController import UserController
from Controllers.TicketsController import TicketController


class SelectTechView(tk.Toplevel):
    '''Окно выбора специалиста'''

    def __init__(self, parent, ticket_id, on_success):
        super().__init__(parent)

        self.ticket_id = ticket_id
        self.on_success = on_success

        self.title("Выбор специалиста")
        self.geometry("400x300")

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
        ttk.Label(self, text="Выберите специалиста", font=("Arial", 14, "bold")).pack(pady=10)

        # Список специалистов
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tech_listbox = tk.Listbox(list_frame, height=10)
        self.tech_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tech_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tech_listbox.configure(yscrollcommand=scrollbar.set)

        # Загрузка специалистов
        techs = UserController.get_by_role('tech')
        admins = UserController.get_by_role('admin')

        self.techs = list(techs) + list(admins)
        for tech in self.techs:
            self.tech_listbox.insert(tk.END, f"{tech.full_name or tech.login} ({tech.role})")

        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="Назначить",
            command=self.assign
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def assign(self):
        '''Назначение выбранного специалиста'''
        selection = self.tech_listbox.curselection()
        if selection:
            tech = self.techs[selection[0]]
            result = TicketController.assign(self.ticket_id, tech.id)

            if result['success']:
                messagebox.showinfo("Успех", result['message'])
                self.on_success()
                self.destroy()
            else:
                messagebox.showerror("Ошибка", result['message'])
        else:
            messagebox.showerror("Ошибка", "Выберите специалиста")