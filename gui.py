# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from constants import TOPICS, TYPE_MAP, TYPE_NAMES, LEVELS, COLORS, HELP_TEXTS
from generators import Generators


class MathApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор уравнений и неравенств")
        self.geometry("900x750")
        self.minsize(800, 650)
        self.configure(bg=COLORS['bg_start'])
        self.data = {}

        self.container = tk.Frame(self, bg=COLORS['bg_start'])
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainMenu, TopicSelect, InputPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg_start'])
        self.controller = controller

        main_frame = tk.Frame(self, bg=COLORS['bg_start'])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="✨ Генератор математических примеров ✨",
                 font=("Arial", 24, "bold"), bg=COLORS['bg_start'], fg=COLORS['fg']).pack(pady=(0, 30))

        for text, topic_id in TOPICS:
            btn = tk.Button(main_frame, text=text, font=("Arial", 12),
                            bg=COLORS['accent'], fg='white', relief='flat',
                            width=30, height=1,
                            activebackground=COLORS['accent_hover'],
                            command=lambda t=topic_id: self.select_topic(t))
            btn.pack(pady=4)

        tk.Button(main_frame, text="🚪 Выход", font=("Arial", 12),
                  bg=COLORS['danger'], fg='white', relief='flat',
                  width=20, height=1,
                  command=self.quit).pack(pady=20)

    def select_topic(self, topic_id):
        self.controller.data['topic'] = topic_id
        self.controller.show_frame("TopicSelect")


class TopicSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg_start'])
        self.controller = controller

        main_frame = tk.Frame(self, bg=COLORS['bg_start'])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="🔮 Выберите тип задания", font=("Arial", 20, "bold"),
                 bg=COLORS['bg_start'], fg=COLORS['fg']).pack(pady=(0, 20))

        self.type_frame = tk.Frame(main_frame, bg=COLORS['bg_start'])
        self.type_frame.pack(pady=10)
        tk.Label(self.type_frame, text="Тип:", font=("Arial", 14), bg=COLORS['bg_start'], fg=COLORS['fg']).pack(side='left', padx=10)

        self.level_frame = tk.Frame(main_frame, bg=COLORS['bg_start'])
        self.level_frame.pack(pady=10)
        tk.Label(self.level_frame, text="Сложность:", font=("Arial", 14), bg=COLORS['bg_start'], fg=COLORS['fg']).pack(side='left', padx=10)

        tk.Button(main_frame, text="❓ Помощь", font=("Arial", 12),
                  bg='#F59E0B', fg='white', relief='flat',
                  width=20, height=1,
                  command=self.show_help).pack(pady=10)

        tk.Button(main_frame, text="⬅ Назад", font=("Arial", 12),
                  bg=COLORS['danger'], fg='white', relief='flat',
                  width=20, height=1,
                  command=lambda: controller.show_frame("MainMenu")).pack(pady=5)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        for widget in self.type_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        for widget in self.level_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        topic = self.controller.data.get('topic', 'linear')
        types = TYPE_MAP.get(topic, [])

        for type_id in types:
            text = TYPE_NAMES.get(type_id, type_id)
            btn = tk.Button(self.type_frame, text=text, font=("Arial", 11),
                            bg=COLORS['accent'], fg='white', relief='flat',
                            width=12, height=1,
                            activebackground=COLORS['accent_hover'],
                            command=lambda t=type_id: self.select_type(t))
            btn.pack(side='left', padx=5)

        level_colors = [COLORS['level_easy'], COLORS['level_medium'], COLORS['level_hard']]
        for i, (level_id, level_name) in enumerate(LEVELS.items()):
            btn = tk.Button(self.level_frame, text=level_name, font=("Arial", 11),
                            bg=level_colors[i], fg='white', relief='flat',
                            width=12, height=1,
                            activebackground='#6B5B9A',
                            command=lambda l=level_id: self.select_level(l))
            btn.pack(side='left', padx=5)

    def select_type(self, type_id):
        self.controller.data['type'] = type_id

    def select_level(self, level_id):
        self.controller.data['level'] = level_id
        if 'type' in self.controller.data and 'level' in self.controller.data:
            self.controller.show_frame("InputPage")

    def show_help(self):
        topic = self.controller.data.get('topic', 'linear')
        help_text = HELP_TEXTS.get(topic, "Описание отсутствует.")
        win = tk.Toplevel(self)
        win.title("Помощь")
        win.geometry("650x500")
        win.configure(bg=COLORS['bg_start'])

        main = tk.Frame(win, bg=COLORS['bg_start'])
        main.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(main)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(main, wrap="word", font=("Arial", 12),
                              bg=COLORS['entry_bg'], fg=COLORS['fg'],
                              yscrollcommand=scrollbar.set,
                              relief='flat', borderwidth=0)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

        tk.Button(main, text="Закрыть", font=("Arial", 12),
                  bg=COLORS['danger'], fg='white', relief='flat',
                  width=15, height=1,
                  command=win.destroy).pack(pady=10)


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg_start'])
        self.controller = controller
        self.entries = []
        self.current_example = ""
        self.solve_params = {}

        main_frame = tk.Frame(self, bg=COLORS['bg_start'])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="📝 Введите данные", font=("Arial", 20, "bold"),
                 bg=COLORS['bg_start'], fg=COLORS['fg']).pack(pady=(0, 15))

        self.input_frame = tk.Frame(main_frame, bg=COLORS['bg_start'])
        self.input_frame.pack(pady=10)

        self.result_frame = tk.Frame(main_frame, bg=COLORS['bg_start'])
        self.result_frame.pack(pady=10, fill='x')

        btn_frame = tk.Frame(main_frame, bg=COLORS['bg_start'])
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="🚀 Сгенерировать", font=("Arial", 12),
                  bg=COLORS['success'], fg='white', relief='flat',
                  width=20, height=1,
                  command=self.generate).pack(side='left', padx=10)

        tk.Button(btn_frame, text="⬅ Назад", font=("Arial", 12),
                  bg=COLORS['danger'], fg='white', relief='flat',
                  width=15, height=1,
                  command=lambda: controller.show_frame("TopicSelect")).pack(side='left', padx=10)

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
        tk.Label(self.input_frame, text=f"Уровень сложности: {level_name}",
                 font=("Arial", 12, "bold"), bg=COLORS['bg_start'], fg=COLORS['highlight']).grid(row=0, column=0, columnspan=2, pady=(0, 10))

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
            frame = tk.Frame(self.input_frame, bg=COLORS['bg_start'])
            frame.grid(row=row, column=0, sticky="ew", pady=5, columnspan=2)
            frame.grid_columnconfigure(0, weight=0)
            frame.grid_columnconfigure(1, weight=1)

            lbl = tk.Label(frame, text=label, font=("Arial", 11), bg=COLORS['bg_start'], fg=COLORS['fg'])
            lbl.grid(row=0, column=0, padx=(0, 10), sticky="w")

            if "Тип решения" in label:
                combo = ttk.Combobox(frame, values=['gt', 'lt', 'ge', 'le'],
                                     state='readonly', font=("Arial", 11))
                combo.grid(row=0, column=1, sticky="ew")
                combo.set('gt')
                self.entries.append(combo)
                hint_frame = tk.Frame(self.input_frame, bg=COLORS['bg_start'])
                hint_frame.grid(row=row+1, column=0, sticky="ew", pady=(0, 10), columnspan=2)
                hint_frame.grid_columnconfigure(0, weight=1)
                hint_text = "gt - больше, lt - меньше, ge - больше или равно, le - меньше или равно"
                tk.Label(hint_frame, text=hint_text, font=("Arial", 9),
                         bg=COLORS['bg_start'], fg='#A5B4FC', justify='left').grid(row=0, column=0, sticky="w")
                row += 1
            else:
                entry = tk.Entry(frame, font=("Arial", 11),
                                 bg=COLORS['entry_bg'], fg=COLORS['fg'],
                                 insertbackground=COLORS['fg'],
                                 relief='flat', borderwidth=1)
                entry.grid(row=0, column=1, sticky="ew")
                self.entries.append(entry)
            row += 1

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
        tk.Label(self.result_frame, text="✨ Сгенерированный пример:", font=("Arial", 14, "bold"),
                 bg=COLORS['bg_start'], fg=COLORS['fg']).pack(anchor='w')
        tk.Label(self.result_frame, text=result, font=("Arial", 13),
                 bg=COLORS['bg_start'], fg=COLORS['highlight'], wraplength=600, justify='left').pack(anchor='w', pady=(5, 10))
        tk.Button(self.result_frame, text="📝 Показать решение", font=("Arial", 11),
                  bg='#F59E0B', fg='white', relief='flat',
                  width=20, height=1,
                  command=self.show_solution).pack(anchor='w', pady=5)

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

        sol_win = tk.Toplevel(self)
        sol_win.title("Решение")
        sol_win.geometry("650x500")
        sol_win.configure(bg=COLORS['bg_start'])

        main = tk.Frame(sol_win, bg=COLORS['bg_start'])
        main.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(main)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(main, wrap="word", font=("Arial", 12),
                              bg=COLORS['entry_bg'], fg=COLORS['fg'],
                              yscrollcommand=scrollbar.set,
                              relief='flat', borderwidth=0)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert("1.0", solution_text)
        text_widget.config(state="disabled")

        tk.Button(main, text="Закрыть", font=("Arial", 12),
                  bg=COLORS['danger'], fg='white', relief='flat',
                  width=15, height=1,
                  command=sol_win.destroy).pack(pady=10)