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

# Пояснения для типов решения неравенств
INEQ_TYPE_HINTS = {
    'gt': 'больше (> 0)',
    'lt': 'меньше (< 0)',
    'ge': 'больше или равно (>= 0)',
    'le': 'меньше или равно (<= 0)'
}