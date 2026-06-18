# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from constants import TOPICS, TYPE_MAP, TYPE_NAMES, LEVELS, COLORS, HELP_TEXTS
from generators import Generators

class GradientFrame(tk.Frame):
    def __init__(self, parent, color_start, color_end, **kwargs):
        super().__init__(parent, **kwargs)
        self.color_start = color_start
        self.color_end = color_end
        self.bind("<Configure>", self._draw_gradient)
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=color_start)
        self.canvas.pack(fill="both", expand=True)

    def _draw_gradient(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        for i in range(height):
            ratio = i / height if height > 0 else 0
            r = int(int(self.color_start[1:3], 16) * (1 - ratio) + int(self.color_end[1:3], 16) * ratio)
            g = int(int(self.color_start[3:5], 16) * (1 - ratio) + int(self.color_end[3:5], 16) * ratio)
            b = int(int(self.color_start[5:7], 16) * (1 - ratio) + int(self.color_end[5:7], 16) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def add_widget(self, widget, **kwargs):
        # Возвращаем ID окна для последующего изменения размеров
        return self.canvas.create_window(0, 0, window=widget, anchor="nw", **kwargs)

    def update_widget_size(self, widget_id, width, height):
        self.canvas.itemconfig(widget_id, width=width, height=height)


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, bg=COLORS['accent'], fg='white',
                 hover_bg=COLORS['accent_hover'], font=("Arial", 12), **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent['bg'], **kwargs)
        self.command = command
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.text = text
        self.font = font
        self._original_bg = bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Configure>", self._draw)
        self._draw()

    def _draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = 15
        self.create_round_rect(0, 0, w, h, r, fill=self.bg, outline='')
        self.create_text(w//2, h//2, text=self.text, fill=self.fg, font=self.font)

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = (x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2, x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1)
        self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        self.bg = self.hover_bg
        self._draw()

    def on_leave(self, event):
        self.bg = self._original_bg
        self._draw()

    def on_click(self, event):
        if self.command:
            self.command()


class MathApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор уравнений и неравенств")
        self.geometry("900x750")
        self.minsize(800, 650)
        self.resizable(True, True)
        self.configure(bg=COLORS['bg_start'])

        self.data = {}

        self.container = GradientFrame(self, COLORS['bg_start'], COLORS['bg_end'])
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.frame_ids = {}  # для хранения ID окон в Canvas
        pages = (MainMenu, TopicSelect, InputPage)
        for F in pages:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Добавляем в Canvas без фиксированных размеров (позже обновим)
            wid = self.container.add_widget(frame)
            self.frame_ids[page_name] = wid

        # Привязываем событие изменения размера окна
        self.bind("<Configure>", self._resize)
        # Принудительно обновляем размеры после создания
        self.after(10, self._resize)  # небольшая задержка для корректного вычисления размеров

        self.show_frame("MainMenu")

    def _resize(self, event=None):
        # Получаем текущие размеры контейнера
        width = self.container.winfo_width()
        height = self.container.winfo_height()
        if width < 10 or height < 10:
            return  # защита от слишком маленьких значений
        for page_name, wid in self.frame_ids.items():
            self.container.update_widget_size(wid, width, height)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.update_idletasks()
        self.container._draw_gradient()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg_start'])
        self.controller = controller

        self.main_frame = tk.Frame(self, bg=COLORS['bg_start'])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(self.main_frame, text="✨ Генератор математических примеров ✨",
                         font=("Arial", 24, "bold"), bg=COLORS['bg_start'], fg=COLORS['fg'])
        title.pack(pady=(0, 30))

        for text, topic_id in TOPICS:
            btn = RoundedButton(self.main_frame, text=text,
                                bg=COLORS['accent'], hover_bg=COLORS['accent_hover'],
                                fg='white', font=("Arial", 12),
                                width=300, height=40,
                                command=lambda t=topic_id: self.select_topic(t))
            btn.pack(pady=6)

        exit_btn = RoundedButton(self.main_frame, text="🚪 Выход",
                                 bg=COLORS['danger'], hover_bg='#F87171',
                                 fg='white', font=("Arial", 12),
                                 width=200, height=40,
                                 command=self.quit)
        exit_btn.pack(pady=20)

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

        help_btn = RoundedButton(main_frame, text="❓ Помощь",
                                 bg='#F59E0B', hover_bg='#FBBF24',
                                 fg='white', font=("Arial", 12),
                                 width=200, height=35,
                                 command=self.show_help)
        help_btn.pack(pady=10)

        back_btn = RoundedButton(main_frame, text="⬅ Назад",
                                 bg=COLORS['danger'], hover_bg='#F87171',
                                 fg='white', font=("Arial", 12),
                                 width=200, height=35,
                                 command=lambda: controller.show_frame("MainMenu"))
        back_btn.pack(pady=5)

        self.main_frame = main_frame

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        # Очищаем старые кнопки типов и уровней
        for widget in self.type_frame.winfo_children():
            if isinstance(widget, RoundedButton):
                widget.destroy()
        for widget in self.level_frame.winfo_children():
            if isinstance(widget, RoundedButton):
                widget.destroy()

        topic = self.controller.data.get('topic', 'linear')
        types = TYPE_MAP.get(topic, [])

        for type_id in types:
            text = TYPE_NAMES.get(type_id, type_id)
            btn = RoundedButton(self.type_frame, text=text,
                                bg=COLORS['accent'], hover_bg=COLORS['accent_hover'],
                                fg='white', font=("Arial", 11),
                                width=120, height=30,
                                command=lambda t=type_id: self.select_type(t))
            btn.pack(side='left', padx=5)

        level_colors = [COLORS['level_easy'], COLORS['level_medium'], COLORS['level_hard']]
        for i, (level_id, level_name) in enumerate(LEVELS.items()):
            btn = RoundedButton(self.level_frame, text=level_name,
                                bg=level_colors[i], hover_bg='#FFFFFF40',
                                fg='white', font=("Arial", 11),
                                width=120, height=30,
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

        grad = GradientFrame(win, COLORS['bg_start'], COLORS['bg_end'])
        grad.pack(fill="both", expand=True)

        text_frame = tk.Frame(grad, bg=COLORS['bg_start'])
        grad.add_widget(text_frame)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 12),
                              bg=COLORS['entry_bg'], fg=COLORS['fg'],
                              yscrollcommand=scrollbar.set,
                              relief='flat', borderwidth=0)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

        close_btn = RoundedButton(grad, text="Закрыть",
                                  bg=COLORS['danger'], hover_bg='#F87171',
                                  fg='white', font=("Arial", 12),
                                  width=150, height=35,
                                  command=win.destroy)
        # Размещаем кнопку внизу
        grad.add_widget(close_btn, anchor="s", y=450)


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

        generate_btn = RoundedButton(btn_frame, text="🚀 Сгенерировать",
                                     bg=COLORS['success'], hover_bg='#A78BFA',
                                     fg='white', font=("Arial", 12),
                                     width=200, height=40,
                                     command=self.generate)
        generate_btn.pack(side='left', padx=10)

        back_btn = RoundedButton(btn_frame, text="⬅ Назад",
                                 bg=COLORS['danger'], hover_bg='#F87171',
                                 fg='white', font=("Arial", 12),
                                 width=150, height=40,
                                 command=lambda: controller.show_frame("TopicSelect"))
        back_btn.pack(side='left', padx=10)

        self.main_frame = main_frame

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
                                     state='readonly', font=("Arial", 11),
                                     background=COLORS['entry_bg'], foreground=COLORS['fg'])
                combo.grid(row=0, column=1, sticky="ew")
                combo.set('gt')
                self.entries.append(combo)
                hint_frame = tk.Frame(self.input_frame, bg=COLORS['bg_start'])
                hint_frame.grid(row=row+1, column=0, sticky="ew", pady=(0, 10), columnspan=2)
                hint_frame.grid_columnconfigure(0, weight=1)
                hint_text = "gt - больше, lt - меньше, ge - больше или равно, le - меньше или равно"
                hint_lbl = tk.Label(hint_frame, text=hint_text, font=("Arial", 9),
                                    bg=COLORS['bg_start'], fg='#A5B4FC', justify='left')
                hint_lbl.grid(row=0, column=0, sticky="w")
                row += 1
            else:
                entry = tk.Entry(frame, font=("Arial", 11),
                                 bg=COLORS['entry_bg'], fg=COLORS['fg'],
                                 insertbackground=COLORS['fg'],
                                 relief='flat', borderwidth=1,
                                 highlightcolor=COLORS['accent'],
                                 highlightthickness=1)
                entry.grid(row=0, column=1, sticky="ew")
                self.entries.append(entry)
            row += 1

        if not self.entries:
            tk.Label(self.input_frame, text="Нет полей для ввода", bg=COLORS['bg_start'], fg=COLORS['fg']).grid()

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
        result_label = tk.Label(self.result_frame, text=result, font=("Arial", 13),
                                bg=COLORS['bg_start'], fg=COLORS['highlight'], wraplength=600, justify='left')
        result_label.pack(anchor='w', pady=(5, 10))
        solve_btn = RoundedButton(self.result_frame, text="📝 Показать решение",
                                  bg='#F59E0B', hover_bg='#FBBF24',
                                  fg='white', font=("Arial", 11),
                                  width=200, height=30,
                                  command=self.show_solution)
        solve_btn.pack(anchor='w', pady=5)

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

        grad = GradientFrame(sol_win, COLORS['bg_start'], COLORS['bg_end'])
        grad.pack(fill="both", expand=True)

        text_frame = tk.Frame(grad, bg=COLORS['bg_start'])
        grad.add_widget(text_frame)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 12),
                              bg=COLORS['entry_bg'], fg=COLORS['fg'],
                              yscrollcommand=scrollbar.set,
                              relief='flat', borderwidth=0)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert("1.0", solution_text)
        text_widget.config(state="disabled")

        close_btn = RoundedButton(grad, text="Закрыть",
                                  bg=COLORS['danger'], hover_bg='#F87171',
                                  fg='white', font=("Arial", 12),
                                  width=150, height=35,
                                  command=sol_win.destroy)
        grad.add_widget(close_btn, anchor="s", y=450)