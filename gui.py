# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from constants import TOPICS, TYPE_MAP, TYPE_NAMES, COLORS
from generators import Generators   # <-- исправлено: добавлен импорт

class MathApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор уравнений и неравенств")
        self.geometry("700x600")
        self.resizable(True, True)
        self.configure(bg=COLORS['bg'])

        self.data = {}

        container = tk.Frame(self, bg=COLORS['bg'])
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        pages = (MainMenu, TopicSelect, InputPage)
        for F in pages:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(len(TOPICS)+1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text="Генератор математических примеров",
                         font=("Arial", 20, "bold"), bg=COLORS['bg'], fg=COLORS['fg'])
        title.grid(row=0, column=0, pady=30, sticky="n")

        row = 1
        for text, topic_id in TOPICS:
            btn = tk.Button(self, text=text, font=("Arial", 12),
                            bg=COLORS['accent'], fg='white', activebackground=COLORS['accent_hover'],
                            command=lambda t=topic_id: self.select_topic(t))
            btn.grid(row=row, column=0, pady=5, padx=20, sticky="ew")
            row += 1

        exit_btn = tk.Button(self, text="Выход", font=("Arial", 12),
                             bg=COLORS['danger'], fg='white', activebackground='#a05070',
                             command=self.quit)
        exit_btn.grid(row=row, column=0, pady=30, padx=20, sticky="ew")

    def select_topic(self, topic_id):
        self.controller.data['topic'] = topic_id
        self.controller.show_frame("TopicSelect")


class TopicSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Выберите тип задания", font=("Arial", 18, "bold"),
                 bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, pady=30, sticky="n")

        self.btn_frame = tk.Frame(self, bg=COLORS['bg'])
        self.btn_frame.grid(row=1, column=0, pady=20, sticky="n")
        self.btn_frame.grid_columnconfigure(0, weight=1)

        back_btn = tk.Button(self, text="Назад", font=("Arial", 12),
                             bg=COLORS['danger'], fg='white', activebackground='#a05070',
                             command=lambda: controller.show_frame("MainMenu"))
        back_btn.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        for widget in self.btn_frame.winfo_children():
            widget.destroy()

        topic = self.controller.data.get('topic', 'linear')
        types = TYPE_MAP.get(topic, [])
        for type_id in types:
            text = TYPE_NAMES.get(type_id, type_id)
            btn = tk.Button(self.btn_frame, text=text, font=("Arial", 14),
                            bg=COLORS['accent'], fg='white', activebackground=COLORS['accent_hover'],
                            command=lambda t=type_id: self.select_type(t))
            btn.pack(pady=10, fill='x', padx=20)

    def select_type(self, type_id):
        self.controller.data['type'] = type_id
        self.controller.show_frame("InputPage")


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller
        self.entries = []

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Введите данные", font=("Arial", 18, "bold"),
                 bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, pady=20, sticky="n")

        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        self.input_frame.grid(row=0, column=0, sticky="ew", pady=10)
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.result_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        self.result_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(0, weight=0)
        self.result_frame.grid_rowconfigure(1, weight=1)

        btn_frame = tk.Frame(self, bg=COLORS['bg'])
        btn_frame.grid(row=2, column=0, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        generate_btn = tk.Button(btn_frame, text="Сгенерировать", font=("Arial", 14),
                                 bg=COLORS['success'], fg='white', activebackground='#9b7ac7')
        generate_btn.grid(row=0, column=0, padx=10, sticky="ew")
        generate_btn.config(command=self.generate)

        back_btn = tk.Button(btn_frame, text="Назад", font=("Arial", 14),
                             bg=COLORS['danger'], fg='white', activebackground='#a05070')
        back_btn.grid(row=0, column=1, padx=10, sticky="ew")
        back_btn.config(command=lambda: controller.show_frame("TopicSelect"))

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.entries.clear()
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        topic = self.controller.data.get('topic', 'linear')
        type_ = self.controller.data.get('type', 'eq')

        # Формируем список меток для полей ввода
        labels = []
        if topic == 'linear':
            if type_ == 'eq':
                labels = ["Корень уравнения (число):"]
            else:
                labels = ["Граница (число):", "Тип решения:"]
        elif topic == 'quadratic':
            if type_ == 'eq':
                labels = ["Корни через пробел (1 или 2 числа):"]
            else:
                labels = ["Корни через пробел (2 числа):", "Тип решения:"]
        elif topic == 'cubic':
            labels = ["Корни через пробел (до 3 чисел):"]
        elif topic == 'rational':
            if type_ == 'eq':
                labels = ["Корень (число):"]
            else:
                labels = ["Корень (число):", "Тип решения:"]
        elif topic == 'irrational':
            if type_ == 'eq':
                labels = ["Корень (число):"]
            else:
                labels = ["Корень (число):", "Тип решения:"]
        elif topic == 'exponential':
            if type_ == 'eq':
                labels = ["Корень (число):"]
            else:
                labels = ["Корень (число):", "Тип решения:"]
        elif topic == 'logarithmic':
            if type_ == 'eq':
                labels = ["Корень (число):"]
            else:
                labels = ["Корень (число):", "Тип решения:"]
        elif topic == 'trigonometric':
            if type_ == 'eq':
                labels = ["Корень (число, радианы):"]
            else:
                labels = ["Корень (число, радианы):", "Тип решения:"]
        elif topic == 'sys_linear':
            labels = ["x =", "y ="]
        elif topic == 'sys_nonlinear':
            labels = ["x =", "y ="]
        else:
            labels = ["Введите данные:"]

        # Создаём поля ввода
        for i, label in enumerate(labels):
            frame = tk.Frame(self.input_frame, bg=COLORS['bg'])
            frame.grid(row=i, column=0, sticky="ew", pady=5)
            frame.grid_columnconfigure(0, weight=0)
            frame.grid_columnconfigure(1, weight=1)

            lbl = tk.Label(frame, text=label, font=("Arial", 12), bg=COLORS['bg'], fg=COLORS['fg'])
            lbl.grid(row=0, column=0, padx=(0, 10), sticky="w")

            if "Тип решения" in label:
                combo = ttk.Combobox(frame, values=['gt', 'lt', 'ge', 'le'], state='readonly', font=("Arial", 12))
                combo.grid(row=0, column=1, sticky="ew")
                combo.set('gt')
                self.entries.append(combo)
                # Подсказка
                hint_frame = tk.Frame(self.input_frame, bg=COLORS['bg'])
                hint_frame.grid(row=i+1, column=0, sticky="ew", pady=(0, 10))
                hint_frame.grid_columnconfigure(0, weight=1)
                hint_text = "gt - больше, lt - меньше, ge - больше или равно, le - меньше или равно"
                hint_lbl = tk.Label(hint_frame, text=hint_text, font=("Arial", 10),
                                    bg=COLORS['bg'], fg='#c9b0e0', justify='left')
                hint_lbl.grid(row=0, column=0, sticky="w")
            else:
                entry = tk.Entry(frame, font=("Arial", 12), bg='#3a2560', fg='white',
                                 insertbackground='white')
                entry.grid(row=0, column=1, sticky="ew")
                self.entries.append(entry)

        if not self.entries:
            tk.Label(self.input_frame, text="Нет полей для ввода", bg=COLORS['bg'], fg=COLORS['fg']).grid()

    def generate(self):
        try:
            topic = self.controller.data.get('topic')
            type_ = self.controller.data.get('type')
            # Собираем значения
            values = []
            for widget in self.entries:
                if isinstance(widget, ttk.Combobox):
                    values.append(widget.get())
                else:
                    values.append(widget.get().strip())

            result = ""
            if topic == 'linear':
                if type_ == 'eq':
                    root = float(values[0])
                    result = Generators.linear_equation(root)
                else:
                    boundary = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.linear_inequality(boundary, sol_type)
            elif topic == 'quadratic':
                if type_ == 'eq':
                    roots = list(map(float, values[0].split()))
                    if len(roots) == 0 or len(roots) > 2:
                        raise ValueError("Введите 1 или 2 числа")
                    result = Generators.quadratic_equation(roots)
                else:
                    roots = list(map(float, values[0].split()))
                    if len(roots) != 2:
                        raise ValueError("Введите 2 числа")
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.quadratic_inequality(roots, sol_type)
            elif topic == 'cubic':
                roots = list(map(float, values[0].split()))
                if len(roots) == 0:
                    roots = []
                result = Generators.cubic_equation(roots)
            elif topic == 'rational':
                if type_ == 'eq':
                    root = float(values[0])
                    result = Generators.rational_equation(root)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.rational_inequality(root, sol_type)
            elif topic == 'irrational':
                if type_ == 'eq':
                    root = float(values[0])
                    result = Generators.irrational_equation(root)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.irrational_inequality(root, sol_type)
            elif topic == 'exponential':
                if type_ == 'eq':
                    root = float(values[0])
                    result = Generators.exponential_equation(root)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.exponential_inequality(root, sol_type)
            elif topic == 'logarithmic':
                if type_ == 'eq':
                    root = float(values[0])
                    result = Generators.logarithmic_equation(root)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.logarithmic_inequality(root, sol_type)
            elif topic == 'trigonometric':
                if type_ == 'eq':
                    root = float(values[0])
                    result = Generators.trigonometric_equation(root)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result = Generators.trigonometric_inequality(root, sol_type)
            elif topic == 'sys_linear':
                x = float(values[0])
                y = float(values[1])
                eq1, eq2 = Generators.system_linear(x, y)
                result = f"{eq1}\n{eq2}"
            elif topic == 'sys_nonlinear':
                x = float(values[0])
                y = float(values[1])
                eq1, eq2 = Generators.system_nonlinear(x, y)
                result = f"{eq1}\n{eq2}"
            else:
                result = "Неизвестная тема"

            # Показываем результат
            for widget in self.result_frame.winfo_children():
                widget.destroy()
            tk.Label(self.result_frame, text="Сгенерированный пример:", font=("Arial", 14, "bold"),
                     bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, pady=(0, 10), sticky="w")
            result_label = tk.Label(self.result_frame, text=result, font=("Arial", 14),
                                    bg=COLORS['bg'], fg=COLORS['highlight'], wraplength=600, justify='left')
            result_label.grid(row=1, column=0, sticky="nw")
            self.result_frame.grid_rowconfigure(1, weight=1)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))