# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from constants import TOPICS, TYPE_MAP, TYPE_NAMES, LEVELS, COLORS, HELP_TEXTS
from generators import Generators

class MathApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор уравнений и неравенств")
        self.geometry("800x700")
        self.resizable(True, True)
        self.configure(bg=COLORS['bg'])

        self.data = {}

        container = tk.Frame(self, bg=COLORS['bg'])
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        pages = (MainMenu, TopicSelect, InputPage)  # HelpPage больше нет
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
        self.grid_rowconfigure(len(TOPICS)+2, weight=1)
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

        # Кнопка "Помощь" открывает отдельное окно
        help_btn = tk.Button(self, text="❓ Помощь", font=("Arial", 12),
                             bg='#f39c12', fg='white', activebackground='#e67e22',
                             command=self.show_help_window)
        help_btn.grid(row=row, column=0, pady=10, padx=20, sticky="ew")
        row += 1

        exit_btn = tk.Button(self, text="Выход", font=("Arial", 12),
                             bg=COLORS['danger'], fg='white', activebackground='#a05070',
                             command=self.quit)
        exit_btn.grid(row=row, column=0, pady=30, padx=20, sticky="ew")

    def select_topic(self, topic_id):
        self.controller.data['topic'] = topic_id
        self.controller.show_frame("TopicSelect")

    def show_help_window(self):
        """Открывает отдельное окно с помощью для выбранной темы."""
        topic = self.controller.data.get('topic', 'linear')
        help_text = HELP_TEXTS.get(topic, "Описание для этого раздела пока отсутствует.")

        help_win = tk.Toplevel(self)
        help_win.title("Помощь")
        help_win.geometry("650x500")
        help_win.configure(bg=COLORS['bg'])

        text_widget = tk.Text(help_win, wrap="word", font=("Arial", 12),
                              bg=COLORS['bg_light'], fg=COLORS['fg'])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

        close_btn = tk.Button(help_win, text="Закрыть", font=("Arial", 12),
                              bg=COLORS['danger'], fg='white', command=help_win.destroy)
        close_btn.pack(pady=10)


class TopicSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Выберите тип задания", font=("Arial", 18, "bold"),
                 bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, pady=20, sticky="n")

        self.type_frame = tk.Frame(self, bg=COLORS['bg'])
        self.type_frame.grid(row=1, column=0, pady=10, sticky="n")
        self.type_frame.grid_columnconfigure(0, weight=1)

        self.level_frame = tk.Frame(self, bg=COLORS['bg'])
        self.level_frame.grid(row=2, column=0, pady=10, sticky="n")
        self.level_frame.grid_columnconfigure(0, weight=1)

        back_btn = tk.Button(self, text="Назад", font=("Arial", 12),
                             bg=COLORS['danger'], fg='white', activebackground='#a05070',
                             command=lambda: controller.show_frame("MainMenu"))
        back_btn.grid(row=3, column=0, pady=20, padx=20, sticky="ew")

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        for widget in self.type_frame.winfo_children():
            widget.destroy()
        for widget in self.level_frame.winfo_children():
            widget.destroy()

        topic = self.controller.data.get('topic', 'linear')
        types = TYPE_MAP.get(topic, [])

        tk.Label(self.type_frame, text="Тип задания:", font=("Arial", 14),
                 bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, pady=5)
        for i, type_id in enumerate(types):
            text = TYPE_NAMES.get(type_id, type_id)
            btn = tk.Button(self.type_frame, text=text, font=("Arial", 12),
                            bg=COLORS['accent'], fg='white', activebackground=COLORS['accent_hover'],
                            command=lambda t=type_id: self.select_type(t))
            btn.grid(row=1, column=i, padx=10, pady=5, sticky="ew")
            self.type_frame.grid_columnconfigure(i, weight=1)

        tk.Label(self.level_frame, text="Уровень сложности:", font=("Arial", 14),
                 bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, columnspan=3, pady=10)
        level_colors = [COLORS['level_easy'], COLORS['level_medium'], COLORS['level_hard']]
        for i, (level_id, level_name) in enumerate(LEVELS.items()):
            btn = tk.Button(self.level_frame, text=level_name, font=("Arial", 12),
                            bg=level_colors[i], fg='white',
                            command=lambda l=level_id: self.select_level(l))
            btn.grid(row=1, column=i, padx=10, pady=5, sticky="ew")
            self.level_frame.grid_columnconfigure(i, weight=1)

    def select_type(self, type_id):
        self.controller.data['type'] = type_id

    def select_level(self, level_id):
        self.controller.data['level'] = level_id
        if 'type' in self.controller.data and 'level' in self.controller.data:
            self.controller.show_frame("InputPage")


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller
        self.entries = []
        self.current_example = ""
        self.solve_params = {}

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
        self.result_frame.grid_rowconfigure(2, weight=0)

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
        self.current_example = ""
        self.solve_params = {}

        topic = self.controller.data.get('topic', 'linear')
        type_ = self.controller.data.get('type', 'eq')
        level = self.controller.data.get('level', 'easy')

        level_name = LEVELS.get(level, '')
        tk.Label(self.input_frame, text=f"Уровень сложности: {level_name}", font=("Arial", 12, "bold"),
                 bg=COLORS['bg'], fg=COLORS['highlight']).grid(row=0, column=0, columnspan=2, pady=(0, 10))

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

        row = 1
        for i, label in enumerate(labels):
            frame = tk.Frame(self.input_frame, bg=COLORS['bg'])
            frame.grid(row=row, column=0, sticky="ew", pady=5, columnspan=2)
            frame.grid_columnconfigure(0, weight=0)
            frame.grid_columnconfigure(1, weight=1)

            lbl = tk.Label(frame, text=label, font=("Arial", 12), bg=COLORS['bg'], fg=COLORS['fg'])
            lbl.grid(row=0, column=0, padx=(0, 10), sticky="w")

            if "Тип решения" in label:
                combo = ttk.Combobox(frame, values=['gt', 'lt', 'ge', 'le'], state='readonly', font=("Arial", 12))
                combo.grid(row=0, column=1, sticky="ew")
                combo.set('gt')
                self.entries.append(combo)
                hint_frame = tk.Frame(self.input_frame, bg=COLORS['bg'])
                hint_frame.grid(row=row+1, column=0, sticky="ew", pady=(0, 10), columnspan=2)
                hint_frame.grid_columnconfigure(0, weight=1)
                hint_text = "gt - больше, lt - меньше, ge - больше или равно, le - меньше или равно"
                hint_lbl = tk.Label(hint_frame, text=hint_text, font=("Arial", 10),
                                    bg=COLORS['bg'], fg='#c9b0e0', justify='left')
                hint_lbl.grid(row=0, column=0, sticky="w")
                row += 1
            else:
                entry = tk.Entry(frame, font=("Arial", 12), bg='#3a2560', fg='white',
                                 insertbackground='white')
                entry.grid(row=0, column=1, sticky="ew")
                self.entries.append(entry)
            row += 1

        if not self.entries:
            tk.Label(self.input_frame, text="Нет полей для ввода", bg=COLORS['bg'], fg=COLORS['fg']).grid()

    def generate(self):
        try:
            topic = self.controller.data.get('topic')
            type_ = self.controller.data.get('type')
            level = self.controller.data.get('level', 'easy')

            values = []
            for widget in self.entries:
                if isinstance(widget, ttk.Combobox):
                    values.append(widget.get())
                else:
                    values.append(widget.get().strip())

            result_str = ""
            params = {}

            if topic == 'linear':
                if type_ == 'eq':
                    root = float(values[0])
                    result_str, params = Generators.linear_equation(root, level)
                else:
                    boundary = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.linear_inequality(boundary, sol_type, level)
            elif topic == 'quadratic':
                if type_ == 'eq':
                    roots = list(map(float, values[0].split()))
                    if len(roots) == 0 or len(roots) > 2:
                        raise ValueError("Введите 1 или 2 числа")
                    result_str, params = Generators.quadratic_equation(roots, level)
                else:
                    roots = list(map(float, values[0].split()))
                    if len(roots) != 2:
                        raise ValueError("Введите 2 числа")
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.quadratic_inequality(roots, sol_type, level)
            elif topic == 'cubic':
                roots = list(map(float, values[0].split()))
                if len(roots) == 0:
                    roots = []
                result_str, params = Generators.cubic_equation(roots, level)
            elif topic == 'rational':
                if type_ == 'eq':
                    root = float(values[0])
                    result_str, params = Generators.rational_equation(root, level)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.rational_inequality(root, sol_type, level)
            elif topic == 'irrational':
                if type_ == 'eq':
                    root = float(values[0])
                    result_str, params = Generators.irrational_equation(root, level)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.irrational_inequality(root, sol_type, level)
            elif topic == 'exponential':
                if type_ == 'eq':
                    root = float(values[0])
                    result_str, params = Generators.exponential_equation(root, level)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.exponential_inequality(root, sol_type, level)
            elif topic == 'logarithmic':
                if type_ == 'eq':
                    root = float(values[0])
                    result_str, params = Generators.logarithmic_equation(root, level)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.logarithmic_inequality(root, sol_type, level)
            elif topic == 'trigonometric':
                if type_ == 'eq':
                    root = float(values[0])
                    result_str, params = Generators.trigonometric_equation(root, level)
                else:
                    root = float(values[0])
                    sol_type = values[1].strip().lower()
                    if sol_type not in ('gt', 'lt', 'ge', 'le'):
                        raise ValueError("Тип решения должен быть gt, lt, ge или le")
                    result_str, params = Generators.trigonometric_inequality(root, sol_type, level)
            elif topic == 'sys_linear':
                x = float(values[0])
                y = float(values[1])
                result_str, params = Generators.system_linear(x, y, level)
            elif topic == 'sys_nonlinear':
                x = float(values[0])
                y = float(values[1])
                result_str, params = Generators.system_nonlinear(x, y, level)
            else:
                result_str = "Неизвестная тема"

            self.current_example = result_str
            self.solve_params = params
            self.show_result(result_str)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_result(self, result):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        tk.Label(self.result_frame, text="Сгенерированный пример:", font=("Arial", 14, "bold"),
                 bg=COLORS['bg'], fg=COLORS['fg']).grid(row=0, column=0, pady=(0, 10), sticky="w")
        result_label = tk.Label(self.result_frame, text=result, font=("Arial", 14),
                                bg=COLORS['bg'], fg=COLORS['highlight'], wraplength=600, justify='left')
        result_label.grid(row=1, column=0, sticky="nw")
        solve_btn = tk.Button(self.result_frame, text="📝 Показать решение", font=("Arial", 12),
                              bg='#f39c12', fg='white', activebackground='#e67e22',
                              command=self.show_solution)
        solve_btn.grid(row=2, column=0, pady=10, sticky="w")
        self.result_frame.grid_rowconfigure(1, weight=1)

    def show_solution(self):
        if not self.current_example or not self.solve_params:
            messagebox.showinfo("Нет примера", "Сначала сгенерируйте пример.")
            return

        topic = self.controller.data.get('topic')
        type_ = self.controller.data.get('type')
        params = self.solve_params

        solution_text = ""

        if topic == 'linear':
            if type_ == 'eq':
                solution_text = Generators.solve_linear_equation(params['a'], params['b'], params['c'])
            else:
                solution_text = Generators.solve_linear_inequality(params['a'], params['b'], params['sign'], params['c'])
        elif topic == 'quadratic':
            if type_ == 'eq':
                solution_text = Generators.solve_quadratic_equation(params['a'], params['b'], params['c'])
            else:
                solution_text = Generators.solve_quadratic_inequality(params['a'], params['b'], params['c'], params['sign'], params['roots'])
        elif topic == 'cubic':
            solution_text = Generators.solve_cubic_equation(params['roots'])
        elif topic == 'rational':
            if type_ == 'eq':
                solution_text = Generators.solve_rational_equation(params['a'], params['b'], params['c'], params['d'], params['root'])
            else:
                solution_text = Generators.solve_rational_inequality(params['a'], params['b'], params['c'], params['d'], params['root'], params['sign'])
        elif topic == 'irrational':
            if type_ == 'eq':
                solution_text = Generators.solve_irrational_equation(params['a'], params['b'], params['c'], params['root'])
            else:
                solution_text = Generators.solve_irrational_inequality(params['a'], params['b'], params['c'], params['root'], params['sign'])
        elif topic == 'exponential':
            if type_ == 'eq':
                solution_text = Generators.solve_exponential_equation(params['base'], params['k'], params['b'], params['root'])
            else:
                solution_text = Generators.solve_exponential_inequality(params['base'], params['k'], params['b'], params['root'], params['sign'])
        elif topic == 'logarithmic':
            if type_ == 'eq':
                solution_text = Generators.solve_logarithmic_equation(params['base'], params['b'], params['root'])
            else:
                solution_text = Generators.solve_logarithmic_inequality(params['base'], params['b'], params['root'], params['sign'])
        elif topic == 'trigonometric':
            if type_ == 'eq':
                solution_text = Generators.solve_trigonometric_equation(params['func'], params['k'], params['val'], params['root'])
            else:
                solution_text = Generators.solve_trigonometric_inequality(params['func'], params['k'], params['val'], params['root'], params['sign'])
        elif topic == 'sys_linear':
            solution_text = Generators.solve_system_linear(params['a1'], params['b1'], params['c1'],
                                                          params['a2'], params['b2'], params['c2'],
                                                          params['x'], params['y'])
        elif topic == 'sys_nonlinear':
            solution_text = Generators.solve_system_nonlinear(params['S'], params['P'], params['x'], params['y'])
        else:
            solution_text = "Решение для этого раздела пока не реализовано."

        # Открываем новое окно с решением
        sol_win = tk.Toplevel(self)
        sol_win.title("Решение")
        sol_win.geometry("650x500")
        sol_win.configure(bg=COLORS['bg'])

        text_widget = tk.Text(sol_win, wrap="word", font=("Arial", 12),
                              bg=COLORS['bg_light'], fg=COLORS['fg'])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", solution_text)
        text_widget.config(state="disabled")

        close_btn = tk.Button(sol_win, text="Закрыть", font=("Arial", 12),
                              bg=COLORS['danger'], fg='white', command=sol_win.destroy)
        close_btn.pack(pady=10)