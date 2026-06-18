# constants.py
TOPICS = [
    ("Линейные (уравнения и неравенства)", "linear"),
    ("Квадратные (уравнения и неравенства)", "quadratic"),
    ("Кубические (уравнения)", "cubic"),
    ("Рациональные (уравнения и неравенства)", "rational"),
    ("Иррациональные (уравнения и неравенства)", "irrational"),
    ("Показательные (уравнения и неравенства)", "exponential"),
    ("Логарифмические (уравнения и неравенства)", "logarithmic"),
    ("Тригонометрические (уравнения и неравенства)", "trigonometric"),
    ("Системы линейных уравнений", "sys_linear"),
    ("Системы нелинейных уравнений", "sys_nonlinear")
]

TYPE_MAP = {
    'linear': ['eq', 'ineq'],
    'quadratic': ['eq', 'ineq'],
    'cubic': ['eq'],
    'rational': ['eq', 'ineq'],
    'irrational': ['eq', 'ineq'],
    'exponential': ['eq', 'ineq'],
    'logarithmic': ['eq', 'ineq'],
    'trigonometric': ['eq', 'ineq'],
    'sys_linear': ['sys'],
    'sys_nonlinear': ['sys']
}

TYPE_NAMES = {
    'eq': 'Уравнение',
    'ineq': 'Неравенство',
    'sys': 'Система'
}

# Цветовая схема (фиолетовая гамма)
COLORS = {
    'bg': '#2c1a4d',          # тёмно-фиолетовый фон
    'bg_light': '#4a2c6a',    # светлее для фреймов
    'fg': '#e0d0f0',          # светлый текст
    'accent': '#8b5fbf',      # акцент для кнопок
    'accent_hover': '#a87cd4',
    'success': '#7b5ea7',     # для кнопки "Сгенерировать"
    'danger': '#8b4a6a',      # для выхода/назад
    'highlight': '#c9a8e8'    # для результата
}