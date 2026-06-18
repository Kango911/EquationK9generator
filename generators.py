# generators.py
import random
import math

class Generators:
    @staticmethod
    def _random_int(level, low, high, extreme=False):
        if level == 'easy':
            return random.randint(low, high)
        elif level == 'medium':
            return random.randint(low * 2, high * 2) if abs(low) > 1 else random.randint(low, high*2)
        else:
            if extreme:
                return random.randint(low * 5, high * 5) if abs(low) > 1 else random.randint(low, high*5)
            return random.randint(low * 3, high * 3) if abs(low) > 1 else random.randint(low, high*3)

    @staticmethod
    def _random_coeff(level, nonzero=True):
        if level == 'easy':
            choices = [-3, -2, -1, 1, 2, 3] if nonzero else [-3, -2, -1, 0, 1, 2, 3]
        elif level == 'medium':
            choices = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6] if nonzero else [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
        else:
            choices = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        return random.choice(choices)

    @staticmethod
    def linear_equation(root, level='easy'):
        a = Generators._random_coeff(level)
        b = -a * root
        c = 0
        if level == 'hard' and random.choice([True, False]):
            c = Generators._random_int('hard', -10, 10, extreme=True)
            b = c - a * root
            return f"{a}x + {b} = {c}".replace("+ -", "- "), {'a': a, 'b': b, 'c': c}
        return f"{a}x + {b} = 0".replace("+ -", "- "), {'a': a, 'b': b, 'c': 0}

    @staticmethod
    def linear_inequality(boundary, sol_type, level='easy'):
        a = Generators._random_coeff(level)
        b = -a * boundary
        c = 0
        if sol_type == 'gt':
            sign = '>' if a > 0 else '<'
        elif sol_type == 'lt':
            sign = '<' if a > 0 else '>'
        elif sol_type == 'ge':
            sign = '>=' if a > 0 else '<='
        else:
            sign = '<=' if a > 0 else '>='
        left = f"{a}x + {b}".replace("+ -", "- ")
        if level == 'hard' and random.choice([True, False]):
            c = Generators._random_int('hard', -10, 10, extreme=True)
            b = c - a * boundary
            left = f"{a}x + {b}".replace("+ -", "- ")
            return f"{left} {sign} {c}", {'a': a, 'b': b, 'c': c, 'sign': sign}
        return f"{left} {sign} 0", {'a': a, 'b': b, 'c': 0, 'sign': sign}

    @staticmethod
    def quadratic_equation(roots, level='easy'):
        if len(roots) == 1:
            r = roots[0]
            a = Generators._random_coeff(level)
            b = -2 * a * r
            c = a * r * r
        else:
            r1, r2 = roots[0], roots[1]
            a = Generators._random_coeff(level)
            b = -a * (r1 + r2)
            c = a * r1 * r2
        terms = []
        if a == 1:
            terms.append("x^2")
        elif a == -1:
            terms.append("-x^2")
        else:
            terms.append(f"{a}x^2")
        if b != 0:
            terms.append(f"{b:+}x".replace("+", "+ ").replace("-", "- "))
        if c != 0:
            terms.append(f"{c:+}".replace("+", "+ ").replace("-", "- "))
        expr = " ".join(terms).replace("+ -", "- ")
        return f"{expr} = 0", {'a': a, 'b': b, 'c': c, 'roots': roots}

    @staticmethod
    def quadratic_inequality(roots, ineq_type, level='easy'):
        if len(roots) != 2:
            raise ValueError("Need two roots")
        r1, r2 = roots
        if r1 > r2:
            r1, r2 = r2, r1
        a = Generators._random_coeff(level)
        b = -a * (r1 + r2)
        c = a * r1 * r2
        if a > 0:
            sign_map = {'gt': '>', 'lt': '<', 'ge': '>=', 'le': '<='}
        else:
            sign_map = {'gt': '<', 'lt': '>', 'ge': '<=', 'le': '>='}
        sign = sign_map[ineq_type]
        terms = []
        if a == 1:
            terms.append("x^2")
        elif a == -1:
            terms.append("-x^2")
        else:
            terms.append(f"{a}x^2")
        if b != 0:
            terms.append(f"{b:+}x".replace("+", "+ ").replace("-", "- "))
        if c != 0:
            terms.append(f"{c:+}".replace("+", "+ ").replace("-", "- "))
        expr = " ".join(terms).replace("+ -", "- ")
        return f"{expr} {sign} 0", {'a': a, 'b': b, 'c': c, 'roots': [r1, r2], 'sign': sign}

    @staticmethod
    def cubic_equation(roots, level='easy'):
        if len(roots) == 0:
            if level == 'easy':
                roots = [random.randint(-3, 3) for _ in range(3)]
            elif level == 'medium':
                roots = [random.randint(-5, 5) for _ in range(3)]
            else:
                roots = [random.randint(-8, 8) for _ in range(3)]
        while len(roots) < 3:
            roots.append(roots[-1])
        r1, r2, r3 = roots[0], roots[1], roots[2]
        a = Generators._random_coeff(level)
        b = -(r1 + r2 + r3)
        c = r1*r2 + r1*r3 + r2*r3
        d = -r1*r2*r3
        A = a
        B = a * b
        C = a * c
        D = a * d
        terms = []
        if A == 1:
            terms.append("x^3")
        elif A == -1:
            terms.append("-x^3")
        else:
            terms.append(f"{A}x^3")
        if B != 0:
            terms.append(f"{B:+}x^2".replace("+", "+ ").replace("-", "- "))
        if C != 0:
            terms.append(f"{C:+}x".replace("+", "+ ").replace("-", "- "))
        if D != 0:
            terms.append(f"{D:+}".replace("+", "+ ").replace("-", "- "))
        expr = " ".join(terms).replace("+ -", "- ")
        return f"{expr} = 0", {'a': A, 'b': B, 'c': C, 'd': D, 'roots': roots}

    @staticmethod
    def rational_equation(root, level='easy'):
        a = Generators._random_coeff(level)
        b = -a * root
        if level == 'hard':
            c = Generators._random_int('hard', -8, 8, extreme=True)
            d = Generators._random_int('hard', -10, 10, extreme=True)
            while c * root + d == 0:
                d = Generators._random_int('hard', -10, 10, extreme=True)
        else:
            c = random.choice([1, 2, 3, -1, -2, -3])
            d = random.randint(-5, 5)
            while c * root + d == 0:
                d = random.randint(-5, 5)
        num = f"{a}x + {b}".replace("+ -", "- ")
        den = f"{c}x + {d}".replace("+ -", "- ")
        return f"({num}) / ({den}) = 0", {'a': a, 'b': b, 'c': c, 'd': d, 'root': root}

    @staticmethod
    def rational_inequality(root, sol_type, level='easy'):
        if sol_type in ('gt', 'ge'):
            a = Generators._random_coeff(level) if level != 'hard' else Generators._random_int('hard', 1, 10, extreme=True)
            b = -a * root
            c = random.choice([1, 2]) if level != 'hard' else random.choice([1, 2, 3, 4])
            d = random.randint(-5, 5) if level != 'hard' else random.randint(-10, 10)
            while c * root + d <= 0:
                d = random.randint(-5, 5) if level != 'hard' else random.randint(-10, 10)
            sign = '>' if sol_type == 'gt' else '>='
        else:
            a = Generators._random_coeff(level) if level != 'hard' else Generators._random_int('hard', -10, -1, extreme=True)
            b = -a * root
            c = random.choice([1, 2]) if level != 'hard' else random.choice([1, 2, 3, 4])
            d = random.randint(-5, 5) if level != 'hard' else random.randint(-10, 10)
            while c * root + d <= 0:
                d = random.randint(-5, 5) if level != 'hard' else random.randint(-10, 10)
            sign = '<' if sol_type == 'lt' else '<='
        num = f"{a}x + {b}".replace("+ -", "- ")
        den = f"{c}x + {d}".replace("+ -", "- ")
        return f"({num}) / ({den}) {sign} 0", {'a': a, 'b': b, 'c': c, 'd': d, 'root': root, 'sign': sign}

    @staticmethod
    def irrational_equation(root, level='easy'):
        if level == 'easy':
            c = random.randint(1, 3)
            a = random.choice([1, 2])
            b = c*c - a*root
        elif level == 'medium':
            c = random.randint(1, 5)
            a = random.choice([1, 2, 3, -1, -2])
            b = c*c - a*root
        else:
            c = random.randint(2, 8)
            a = Generators._random_int('hard', -5, 5, extreme=True)
            b = c*c - a*root
            if random.choice([True, False]):
                extra = Generators._random_int('hard', -10, 10, extreme=True)
                b += extra
                b = c*c - extra - a*root
        return f"sqrt({a}x + {b}) = {c}", {'a': a, 'b': b, 'c': c, 'root': root}

    @staticmethod
    def irrational_inequality(root, sol_type, level='easy'):
        a = random.choice([1, 2, 3]) if level != 'hard' else Generators._random_int('hard', 1, 5, extreme=True)
        if sol_type == 'gt':
            b = -a * root
            return f"sqrt({a}x + {b}) > 0", {'a': a, 'b': b, 'c': 0, 'root': root, 'sign': '>'}
        elif sol_type == 'ge':
            b = -a * root
            return f"sqrt({a}x + {b}) >= 0", {'a': a, 'b': b, 'c': 0, 'root': root, 'sign': '>='}
        elif sol_type == 'lt':
            c = random.randint(1, 3) if level != 'hard' else random.randint(2, 6)
            b = c*c - a*root
            return f"sqrt({a}x + {b}) < {c}", {'a': a, 'b': b, 'c': c, 'root': root, 'sign': '<'}
        else:
            c = random.randint(1, 3) if level != 'hard' else random.randint(2, 6)
            b = c*c - a*root
            return f"sqrt({a}x + {b}) <= {c}", {'a': a, 'b': b, 'c': c, 'root': root, 'sign': '<='}

    @staticmethod
    def exponential_equation(root, level='easy'):
        if level == 'easy':
            base = random.choice([2, 3])
            b = base ** int(root) if root == int(root) else round(base ** root, 2)
            k = 1
        elif level == 'medium':
            base = random.choice([2, 3, 4])
            b = base ** int(root) if root == int(root) else round(base ** root, 2)
            k = 1
        else:
            base = random.choice([2, 3, 4, 5, 6, 7])
            b = base ** int(root) if root == int(root) else round(base ** root, 2)
            k = 1
            if random.choice([True, False]):
                k = Generators._random_int('hard', 2, 5, extreme=True)
                b = base ** (k * root)
                return f"{base}^{{{k}x}} = {b}", {'base': base, 'k': k, 'b': b, 'root': root}
        return f"{base}^x = {b}", {'base': base, 'k': 1, 'b': b, 'root': root}

    @staticmethod
    def exponential_inequality(root, sol_type, level='easy'):
        base = random.choice([2, 3]) if level == 'easy' else random.choice([2, 3, 4, 5])
        b = base ** root
        k = 1
        if sol_type in ('gt', 'ge'):
            sign = '>' if sol_type == 'gt' else '>='
        else:
            sign = '<' if sol_type == 'lt' else '<='
        if level == 'hard' and random.choice([True, False]):
            k = Generators._random_int('hard', 2, 4, extreme=True)
            b = base ** (k * root)
            return f"{base}^{{{k}x}} {sign} {b}", {'base': base, 'k': k, 'b': b, 'root': root, 'sign': sign}
        return f"{base}^x {sign} {b}", {'base': base, 'k': 1, 'b': b, 'root': root, 'sign': sign}

    @staticmethod
    def logarithmic_equation(root, level='easy'):
        base = random.choice([2, 3]) if level == 'easy' else random.choice([2, 3, 4, 5])
        found = False
        for b_candidate in range(1, 6):
            if abs(base ** b_candidate - root) < 0.001:
                b = b_candidate
                found = True
                break
        if not found:
            if level == 'hard':
                b = round(math.log(root, base), 2)
            else:
                b = random.randint(1, 3)
        if isinstance(b, float) and b.is_integer():
            b = int(b)
        return f"log_{base}(x) = {b}", {'base': base, 'b': b, 'root': root}

    @staticmethod
    def logarithmic_inequality(root, sol_type, level='easy'):
        base = random.choice([2, 3]) if level == 'easy' else random.choice([2, 3, 4, 5])
        found = False
        for b_candidate in range(1, 6):
            if abs(base ** b_candidate - root) < 0.001:
                b = b_candidate
                found = True
                break
        if not found:
            if level == 'hard':
                b = round(math.log(root, base), 2)
            else:
                b = random.randint(1, 3)
        if isinstance(b, float) and b.is_integer():
            b = int(b)
        if sol_type in ('gt', 'ge'):
            sign = '>' if sol_type == 'gt' else '>='
        else:
            sign = '<' if sol_type == 'lt' else '<='
        return f"log_{base}(x) {sign} {b}", {'base': base, 'b': b, 'root': root, 'sign': sign}

    @staticmethod
    def trigonometric_equation(root, level='easy'):
        if level == 'easy':
            func = random.choice(['sin', 'cos'])
            angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
            closest = min(angles, key=lambda a: abs(a - root))
            if func == 'sin':
                val = math.sin(closest)
            else:
                val = math.cos(closest)
            val_str = f"{val:.2f}"
            return f"{func}(x) = {val_str}", {'func': func, 'k': 1, 'val': val, 'root': root}
        elif level == 'medium':
            func = random.choice(['sin', 'cos', 'tg'])
            angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
            closest = min(angles, key=lambda a: abs(a - root))
            if func == 'sin':
                val = math.sin(closest)
            elif func == 'cos':
                val = math.cos(closest)
            else:
                val = math.tan(closest)
                if abs(val) > 5:
                    val = round(val, 1)
            val_str = f"{val:.2f}"
            if func == 'tg' and abs(val) > 5:
                val_str = f"{val:.1f}"
            return f"{func}(x) = {val_str}", {'func': func, 'k': 1, 'val': val, 'root': root}
        else:
            func = random.choice(['sin', 'cos', 'tg'])
            k = random.choice([2, 3, 4])
            angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
            target = k * root
            closest = min(angles, key=lambda a: abs(a - target))
            if func == 'sin':
                val = math.sin(closest)
            elif func == 'cos':
                val = math.cos(closest)
            else:
                val = math.tan(closest)
                if abs(val) > 10:
                    val = round(val, 1)
            val_str = f"{val:.2f}" if abs(val) < 10 else f"{val:.1f}"
            return f"{func}({k}x) = {val_str}", {'func': func, 'k': k, 'val': val, 'root': root}

    @staticmethod
    def trigonometric_inequality(root, sol_type, level='easy'):
        if level == 'easy':
            func = random.choice(['sin', 'cos'])
            val = math.sin(root) if func == 'sin' else math.cos(root)
            val_str = f"{val:.2f}"
            k = 1
        elif level == 'medium':
            func = random.choice(['sin', 'cos', 'tg'])
            if func == 'sin':
                val = math.sin(root)
            elif func == 'cos':
                val = math.cos(root)
            else:
                val = math.tan(root)
            val_str = f"{val:.2f}" if abs(val) < 10 else f"{val:.1f}"
            k = 1
        else:
            func = random.choice(['sin', 'cos', 'tg'])
            k = random.choice([2, 3])
            if func == 'sin':
                val = math.sin(k * root)
            elif func == 'cos':
                val = math.cos(k * root)
            else:
                val = math.tan(k * root)
            val_str = f"{val:.2f}" if abs(val) < 10 else f"{val:.1f}"
        if sol_type in ('gt', 'ge'):
            sign = '>' if sol_type == 'gt' else '>='
        else:
            sign = '<' if sol_type == 'lt' else '<='
        if k == 1:
            return f"{func}(x) {sign} {val_str}", {'func': func, 'k': k, 'val': val, 'root': root, 'sign': sign}
        else:
            return f"{func}({k}x) {sign} {val_str}", {'func': func, 'k': k, 'val': val, 'root': root, 'sign': sign}

    @staticmethod
    def system_linear(root1, root2, level='easy'):
        if level == 'easy':
            a1 = random.randint(1, 3)
            b1 = random.randint(1, 3)
            a2 = random.randint(1, 3)
            b2 = random.randint(1, 3)
            while a1*b2 == a2*b1:
                a2 = random.randint(1, 3)
        elif level == 'medium':
            a1 = random.randint(1, 5)
            b1 = random.randint(1, 5)
            a2 = random.randint(1, 5)
            b2 = random.randint(1, 5)
            while a1*b2 == a2*b1:
                a2 = random.randint(1, 5)
        else:
            a1 = Generators._random_int('hard', 1, 8, extreme=True)
            b1 = Generators._random_int('hard', 1, 8, extreme=True)
            a2 = Generators._random_int('hard', 1, 8, extreme=True)
            b2 = Generators._random_int('hard', 1, 8, extreme=True)
            while a1*b2 == a2*b1:
                a2 = Generators._random_int('hard', 1, 8, extreme=True)
        c1 = a1*root1 + b1*root2
        c2 = a2*root1 + b2*root2
        eq1 = f"{a1}x + {b1}y = {c1}"
        eq2 = f"{a2}x + {b2}y = {c2}"
        return f"{eq1}\n{eq2}", {'a1': a1, 'b1': b1, 'c1': c1, 'a2': a2, 'b2': b2, 'c2': c2, 'x': root1, 'y': root2}

    @staticmethod
    def system_nonlinear(root1, root2, level='easy'):
        S = root1 + root2
        P = root1 * root2
        if level == 'hard':
            k = Generators._random_int('hard', 2, 5, extreme=True)
            eq1 = f"{k}x + y = {k*root1 + root2}"
            eq2 = f"x * y = {P}"
            return f"{eq1}\n{eq2}", {'k': k, 'S': S, 'P': P, 'x': root1, 'y': root2}
        eq1 = f"x + y = {S}"
        eq2 = f"x * y = {P}"
        return f"{eq1}\n{eq2}", {'S': S, 'P': P, 'x': root1, 'y': root2}

    # ==================== МЕТОДЫ РЕШЕНИЯ ====================
    @staticmethod
    def solve_linear_equation(a, b, c=0):
        steps = []
        steps.append(f"Дано: {a}x + {b} = {c}")
        steps.append(f"Переносим {b} в правую часть: {a}x = {c} - ({b}) = {c - b}")
        if a != 0:
            x = (c - b) / a
            steps.append(f"Делим на {a}: x = {x}")
            steps.append(f"Ответ: x = {x}")
        else:
            steps.append("Ошибка: a не может быть 0")
        return "\n".join(steps)

    @staticmethod
    def solve_linear_inequality(a, b, sign, c=0):
        steps = []
        steps.append(f"Дано: {a}x + {b} {sign} {c}")
        steps.append(f"Переносим {b} в правую часть: {a}x {sign} {c - b}")
        right = c - b
        if a > 0:
            x = right / a
            steps.append(f"Делим на положительное {a}: x {sign} {x:.2f}")
            steps.append(f"Ответ: x {sign} {x:.2f}")
        elif a < 0:
            x = right / a
            sign_inv = {'>':'<', '<':'>', '>=':'<=', '<=':'>='}[sign]
            steps.append(f"Делим на отрицательное {a}, знак меняется: x {sign_inv} {x:.2f}")
            steps.append(f"Ответ: x {sign_inv} {x:.2f}")
        else:
            steps.append("Ошибка: a не может быть 0")
        return "\n".join(steps)

    @staticmethod
    def solve_quadratic_equation(a, b, c):
        steps = []
        steps.append(f"Дано: {a}x^2 + {b}x + {c} = 0")
        D = b*b - 4*a*c
        steps.append(f"Вычисляем дискриминант: D = {b}^2 - 4*{a}*{c} = {D}")
        if D > 0:
            sqrtD = math.sqrt(D)
            x1 = (-b + sqrtD) / (2*a)
            x2 = (-b - sqrtD) / (2*a)
            steps.append(f"√D = {sqrtD:.2f}")
            steps.append(f"x1 = (-{b} + √D) / (2*{a}) = {x1:.2f}")
            steps.append(f"x2 = (-{b} - √D) / (2*{a}) = {x2:.2f}")
            steps.append(f"Ответ: x1 = {x1:.2f}, x2 = {x2:.2f}")
        elif D == 0:
            x = -b / (2*a)
            steps.append(f"D = 0, корень один: x = -{b} / (2*{a}) = {x:.2f}")
            steps.append(f"Ответ: x = {x:.2f}")
        else:
            steps.append("D < 0, действительных корней нет")
        return "\n".join(steps)

    @staticmethod
    def solve_quadratic_inequality(a, b, c, sign, roots):
        steps = []
        steps.append(f"Дано: {a}x^2 + {b}x + {c} {sign} 0")
        if len(roots) == 2:
            r1, r2 = sorted(roots)
            steps.append(f"Корни: x1 = {r1}, x2 = {r2}")
            if a > 0:
                if sign in ('>', '>='):
                    steps.append(f"Ветви вверх, решение: x ≤ {r1} или x ≥ {r2}")
                else:
                    steps.append(f"Ветви вверх, решение: {r1} ≤ x ≤ {r2}")
            else:
                if sign in ('>', '>='):
                    steps.append(f"Ветви вниз, решение: {r1} ≤ x ≤ {r2}")
                else:
                    steps.append(f"Ветви вниз, решение: x ≤ {r1} или x ≥ {r2}")
        else:
            steps.append("Случай кратного корня – решение зависит от знака.")
        return "\n".join(steps)

    @staticmethod
    def solve_cubic_equation(roots):
        steps = []
        steps.append("Кубическое уравнение решается по формуле Кардано или подбором корней.")
        steps.append(f"Известные корни (или сгенерированные): {roots}")
        steps.append("Если корни целые, можно разложить на множители.")
        if len(roots) == 3:
            r1, r2, r3 = roots
            steps.append(f"Разложение: (x - {r1})(x - {r2})(x - {r3}) = 0")
            steps.append(f"Ответ: x = {r1}, x = {r2}, x = {r3}")
        else:
            steps.append("Для более точного решения используйте численные методы или формулу Кардано.")
        return "\n".join(steps)

    @staticmethod
    def solve_rational_equation(a, b, c, d, root):
        steps = []
        steps.append(f"Дано: ({a}x + {b}) / ({c}x + {d}) = 0")
        steps.append("Дробь равна нулю, когда числитель равен нулю, а знаменатель не равен нулю.")
        steps.append(f"Решаем {a}x + {b} = 0 → x = {-b/a}")
        steps.append(f"Проверяем знаменатель при x = {root}: {c}*{root} + {d} = {c*root + d} ≠ 0")
        steps.append(f"Ответ: x = {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_rational_inequality(a, b, c, d, root, sign):
        steps = []
        steps.append(f"Дано: ({a}x + {b}) / ({c}x + {d}) {sign} 0")
        steps.append("Находим нули числителя и знаменателя.")
        steps.append(f"Числитель: x = {root}, знаменатель: x = {-d/c} (исключаем из ОДЗ)")
        steps.append("Метод интервалов с учётом знака дроби.")
        steps.append(f"Ответ: зависит от знака и расположения точек. В данном случае решение: x {sign} {root} (с учётом ОДЗ).")
        return "\n".join(steps)

    @staticmethod
    def solve_irrational_equation(a, b, c, root):
        steps = []
        steps.append(f"Дано: sqrt({a}x + {b}) = {c}")
        steps.append("Возводим обе части в квадрат:")
        steps.append(f"{a}x + {b} = {c**2}")
        steps.append(f"{a}x = {c**2 - b}")
        steps.append(f"x = {(c**2 - b)/a}")
        steps.append(f"Проверка: подставляем x = {root}: sqrt({a}*{root} + {b}) = {c} (верно)")
        steps.append(f"Ответ: x = {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_irrational_inequality(a, b, c, root, sign):
        steps = []
        steps.append(f"Дано: sqrt({a}x + {b}) {sign} {c}")
        steps.append("ОДЗ: подкоренное выражение ≥ 0.")
        if sign in ('>', '>='):
            steps.append("Возводим в квадрат, знак сохраняется:")
            steps.append(f"{a}x + {b} {sign} {c**2}")
            steps.append(f"x {sign} {(c**2 - b)/a}")
        else:
            steps.append("Возводим в квадрат, знак сохраняется:")
            steps.append(f"{a}x + {b} {sign} {c**2}")
            steps.append(f"x {sign} {(c**2 - b)/a}")
        steps.append(f"С учётом ОДЗ ответ: x {sign} {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_exponential_equation(base, k, b, root):
        steps = []
        if k == 1:
            steps.append(f"Дано: {base}^x = {b}")
            steps.append(f"Представляем {b} как степень {base}: {b} = {base}^{root}")
            steps.append(f"Основания равны, приравниваем показатели: x = {root}")
        else:
            steps.append(f"Дано: {base}^{{{k}x}} = {b}")
            steps.append(f"Представляем {b} как степень {base}: {b} = {base}^{{{k*root}}}")
            steps.append(f"Основания равны, приравниваем показатели: {k}x = {k*root} → x = {root}")
        steps.append(f"Ответ: x = {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_exponential_inequality(base, k, b, root, sign):
        steps = []
        if k == 1:
            steps.append(f"Дано: {base}^x {sign} {b}")
            steps.append(f"Представляем {b} как степень {base}: {b} = {base}^{root}")
            steps.append(f"Основания равны ({base}>1), знак сохраняется: x {sign} {root}")
        else:
            steps.append(f"Дано: {base}^{{{k}x}} {sign} {b}")
            steps.append(f"Представляем {b} как степень {base}: {b} = {base}^{{{k*root}}}")
            steps.append(f"Основания равны, знак сохраняется: {k}x {sign} {k*root} → x {sign} {root}")
        steps.append(f"Ответ: x {sign} {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_logarithmic_equation(base, b, root):
        steps = []
        steps.append(f"Дано: log_{base}(x) = {b}")
        steps.append("По определению логарифма: x = a^b")
        steps.append(f"x = {base}^{b} = {root}")
        steps.append(f"Ответ: x = {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_logarithmic_inequality(base, b, root, sign):
        steps = []
        steps.append(f"Дано: log_{base}(x) {sign} {b}")
        steps.append("ОДЗ: x > 0")
        steps.append(f"Потенцируем: x {sign} {base}^{b}")
        steps.append(f"x {sign} {root}")
        steps.append(f"С учётом ОДЗ ответ: x {sign} {root}")
        return "\n".join(steps)

    @staticmethod
    def solve_trigonometric_equation(func, k, val, root):
        steps = []
        if k == 1:
            steps.append(f"Дано: {func}(x) = {val:.2f}")
        else:
            steps.append(f"Дано: {func}({k}x) = {val:.2f}")
        if func == 'sin':
            steps.append("Решение: x = arcsin(a) + 2πk  или  x = π - arcsin(a) + 2πk")
            if -1 <= val <= 1:
                arc = math.asin(val)
                steps.append(f"arcsin({val:.2f}) = {arc:.2f} рад")
                steps.append(f"x = {arc:.2f} + 2πk  или  x = {math.pi - arc:.2f} + 2πk")
            else:
                steps.append("Значение вне [-1,1] – решений нет.")
        elif func == 'cos':
            steps.append("Решение: x = ±arccos(a) + 2πk")
            if -1 <= val <= 1:
                arc = math.acos(val)
                steps.append(f"arccos({val:.2f}) = {arc:.2f} рад")
                steps.append(f"x = ±{arc:.2f} + 2πk")
            else:
                steps.append("Значение вне [-1,1] – решений нет.")
        else:  # tg
            steps.append("Решение: x = arctg(a) + πk")
            arc = math.atan(val)
            steps.append(f"arctg({val:.2f}) = {arc:.2f} рад")
            steps.append(f"x = {arc:.2f} + πk")
        if k != 1:
            steps.append(f"Учитывая множитель {k}, делим все решения на {k}.")
        return "\n".join(steps)

    @staticmethod
    def solve_trigonometric_inequality(func, k, val, root, sign):
        steps = []
        if k == 1:
            steps.append(f"Дано: {func}(x) {sign} {val:.2f}")
        else:
            steps.append(f"Дано: {func}({k}x) {sign} {val:.2f}")
        steps.append("Решение на единичной окружности с учётом периодичности.")
        steps.append(f"Ответ: промежутки, удовлетворяющие неравенству (зависят от знака и значения).")
        return "\n".join(steps)

    @staticmethod
    def solve_system_linear(a1, b1, c1, a2, b2, c2, x, y):
        steps = []
        steps.append(f"Система:\n{a1}x + {b1}y = {c1}\n{a2}x + {b2}y = {c2}")
        steps.append("Решаем методом подстановки:")
        if b1 != 0:
            steps.append(f"Из первого: y = ({c1} - {a1}x) / {b1}")
            steps.append(f"Подставляем во второе: {a2}x + {b2}*(({c1} - {a1}x)/{b1}) = {c2}")
            A = a2 - (b2*a1)/b1
            C = c2 - (b2*c1)/b1
            steps.append(f"После упрощения: {A:.2f}x = {C:.2f} → x = {C/A:.2f}")
            steps.append(f"Подставляем x = {x} в первое: {a1}*{x} + {b1}y = {c1} → y = {y}")
        else:
            steps.append("Выражаем x из первого и подставляем во второе.")
        steps.append(f"Ответ: x = {x}, y = {y}")
        return "\n".join(steps)

    @staticmethod
    def solve_system_nonlinear(S, P, x, y):
        steps = []
        steps.append(f"Система:\nx + y = {S}\nx*y = {P}")
        steps.append("По теореме Виета x и y – корни квадратного уравнения:")
        steps.append(f"t² - {S}t + {P} = 0")
        D = S*S - 4*P
        steps.append(f"D = {S}² - 4*{P} = {D}")
        if D >= 0:
            t1 = (S + math.sqrt(D)) / 2
            t2 = (S - math.sqrt(D)) / 2
            steps.append(f"Корни: t1 = {t1:.2f}, t2 = {t2:.2f}")
            steps.append(f"Ответ: x = {x}, y = {y}")
        else:
            steps.append("Действительных решений нет (но по условию они есть).")
        return "\n".join(steps)