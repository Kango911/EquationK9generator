# generators.py
import random
import math

class Generators:
    """Статические методы для генерации примеров по всем темам."""

    # ---------- Линейные ----------
    @staticmethod
    def linear_equation(root):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = -a * root
        return f"{a}x + {b} = 0".replace("+ -", "- ")

    @staticmethod
    def linear_inequality(boundary, sol_type):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = -a * boundary
        if sol_type == 'gt':
            sign = '>' if a > 0 else '<'
        elif sol_type == 'lt':
            sign = '<' if a > 0 else '>'
        elif sol_type == 'ge':
            sign = '>=' if a > 0 else '<='
        else:  # le
            sign = '<=' if a > 0 else '>='
        left = f"{a}x + {b}".replace("+ -", "- ")
        return f"{left} {sign} 0"

    # ---------- Квадратные ----------
    @staticmethod
    def quadratic_equation(roots):
        if len(roots) == 1:
            r = roots[0]
            a = random.choice([1, 2, 3, -1, -2, -3])
            b = -2 * a * r
            c = a * r * r
        else:
            r1, r2 = roots[0], roots[1]
            a = random.choice([1, 2, 3, -1, -2, -3])
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
        return f"{expr} = 0"

    @staticmethod
    def quadratic_inequality(roots, ineq_type):
        if len(roots) != 2:
            raise ValueError("Need two roots")
        r1, r2 = roots
        if r1 > r2:
            r1, r2 = r2, r1
        a = random.choice([1, 2, 3, -1, -2, -3])
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
        return f"{expr} {sign} 0"

    # ---------- Кубические ----------
    @staticmethod
    def cubic_equation(roots):
        if len(roots) == 0:
            roots = [random.randint(-5, 5) for _ in range(3)]
        while len(roots) < 3:
            roots.append(roots[-1])
        r1, r2, r3 = roots[0], roots[1], roots[2]
        a = random.choice([1, -1, 2, -2])
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
        return f"{expr} = 0"

    # ---------- Рациональные ----------
    @staticmethod
    def rational_equation(root):
        a = random.choice([1, 2, 3, 4, 5, -1, -2, -3, -4, -5])
        b = -a * root
        c = random.choice([1, 2, 3, -1, -2, -3])
        d = random.randint(-5, 5)
        while c * root + d == 0:
            d = random.randint(-5, 5)
        num = f"{a}x + {b}".replace("+ -", "- ")
        den = f"{c}x + {d}".replace("+ -", "- ")
        return f"({num}) / ({den}) = 0"

    @staticmethod
    def rational_inequality(root, sol_type):
        if sol_type in ('gt', 'ge'):
            a = random.choice([1, 2, 3])
            b = -a * root
            c = random.choice([1, 2])
            d = random.randint(-5, 5)
            while c * root + d <= 0:
                d = random.randint(-5, 5)
            sign = '>' if sol_type == 'gt' else '>='
        else:
            a = random.choice([-1, -2, -3])
            b = -a * root
            c = random.choice([1, 2])
            d = random.randint(-5, 5)
            while c * root + d <= 0:
                d = random.randint(-5, 5)
            sign = '<' if sol_type == 'lt' else '<='
        num = f"{a}x + {b}".replace("+ -", "- ")
        den = f"{c}x + {d}".replace("+ -", "- ")
        return f"({num}) / ({den}) {sign} 0"

    # ---------- Иррациональные ----------
    @staticmethod
    def irrational_equation(root):
        c = random.randint(1, 5)
        a = random.choice([1, 2, 3, -1, -2, -3])
        b = c*c - a*root
        return f"sqrt({a}x + {b}) = {c}".replace("+ -", "- ")

    @staticmethod
    def irrational_inequality(root, sol_type):
        a = random.choice([1, 2, 3])
        if sol_type == 'gt':
            b = -a * root
            return f"sqrt({a}x + {b}) > 0".replace("+ -", "- ")
        elif sol_type == 'ge':
            b = -a * root
            return f"sqrt({a}x + {b}) >= 0".replace("+ -", "- ")
        elif sol_type == 'lt':
            c = random.randint(1, 3)
            b = c*c - a*root
            return f"sqrt({a}x + {b}) < {c}".replace("+ -", "- ")
        else:  # le
            c = random.randint(1, 3)
            b = c*c - a*root
            return f"sqrt({a}x + {b}) <= {c}".replace("+ -", "- ")

    # ---------- Показательные ----------
    @staticmethod
    def exponential_equation(root):
        base = random.choice([2, 3, 4, 5])
        root_int = int(root)
        if root_int != root:
            b = round(base ** root, 3)
        else:
            b = base ** root_int
        if b == 0 or b == 1:
            b = 2
        return f"{base}^x = {b}"

    @staticmethod
    def exponential_inequality(root, sol_type):
        base = random.choice([2, 3, 4, 5])
        b = base ** root
        if sol_type in ('gt', 'ge'):
            sign = '>' if sol_type == 'gt' else '>='
        else:
            sign = '<' if sol_type == 'lt' else '<='
        return f"{base}^x {sign} {b}"

    # ---------- Логарифмические ----------
    @staticmethod
    def logarithmic_equation(root):
        base = random.choice([2, 3, 4, 5])
        b = random.randint(1, 5)
        found = False
        for base_candidate in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            for b_candidate in range(1, 6):
                if abs(base_candidate ** b_candidate - root) < 0.001:
                    base = base_candidate
                    b = b_candidate
                    found = True
                    break
            if found:
                break
        if not found:
            base = random.choice([2, 3, 4, 5])
            b = random.randint(1, 5)
        return f"log_{base}(x) = {b}"

    @staticmethod
    def logarithmic_inequality(root, sol_type):
        base = random.choice([2, 3, 4, 5])
        found = False
        for b_candidate in range(1, 6):
            if abs(base ** b_candidate - root) < 0.001:
                b = b_candidate
                found = True
                break
        if not found:
            b = random.randint(1, 5)
        if sol_type in ('gt', 'ge'):
            sign = '>' if sol_type == 'gt' else '>='
        else:
            sign = '<' if sol_type == 'lt' else '<='
        return f"log_{base}(x) {sign} {b}"

    # ---------- Тригонометрические ----------
    @staticmethod
    def trigonometric_equation(root):
        func = random.choice(['sin', 'cos', 'tg'])
        angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
        closest = min(angles, key=lambda a: abs(a - root))
        if func == 'sin':
            val = math.sin(closest)
        elif func == 'cos':
            val = math.cos(closest)
        else:
            val = math.tan(closest)
        val_str = f"{val:.2f}"
        if func == 'tg' and abs(val) > 10:
            val_str = f"{val:.1f}"
        return f"{func}(x) = {val_str}"

    @staticmethod
    def trigonometric_inequality(root, sol_type):
        func = random.choice(['sin', 'cos'])
        if func == 'sin':
            val = math.sin(root)
        else:
            val = math.cos(root)
        val_str = f"{val:.2f}"
        if sol_type in ('gt', 'ge'):
            sign = '>' if sol_type == 'gt' else '>='
        else:
            sign = '<' if sol_type == 'lt' else '<='
        return f"{func}(x) {sign} {val_str}"

    # ---------- Системы линейные ----------
    @staticmethod
    def system_linear(root1, root2):
        a1 = random.randint(1, 5)
        b1 = random.randint(1, 5)
        a2 = random.randint(1, 5)
        b2 = random.randint(1, 5)
        while a1*b2 == a2*b1:
            a2 = random.randint(1, 5)
        c1 = a1*root1 + b1*root2
        c2 = a2*root1 + b2*root2
        return (f"{a1}x + {b1}y = {c1}", f"{a2}x + {b2}y = {c2}")

    # ---------- Системы нелинейные ----------
    @staticmethod
    def system_nonlinear(root1, root2):
        S = root1 + root2
        P = root1 * root2
        return (f"x + y = {S}", f"x * y = {P}")