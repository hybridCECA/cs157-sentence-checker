from checker import check

"""

a.	If Γ ⊨ (φ ∨ ψ), then Γ ⊨ φ or Γ ⊨ ψ.
b.	If Γ ⊨ (φ ∧ ψ) and Γ ⊨ (φ ∧ ¬ψ), then Γ ⊨ φ.
c.	If Γ ⊨ (φ ∨ ψ) and Γ ⊨ (φ ∨ ¬ψ), then Γ ⊨ φ.
d.	If φ ⊨ ψ and ¬φ ⊨ ψ, then φ is unsatisfiable.
e.	If φ ⊨ ψ or ψ ⊨ φ, then φ and ψ are consistent


a.	If Δ ⊭ ¬φ, then Δ∪{φ} is satisfiable.
b.	If Γ∩Δ ⊨ φ, then Γ ⊨ φ and Δ ⊨ φ.
c.	If Γ∪Δ ⊭ φ, then Γ ⊭ φ and Δ ⊭ φ.
d.	If φ ⊨ ψ and φ ⊨ ¬ψ, then φ is unsatisfiable.
e.	If φ ⊨ ψ and ¬φ ⊨ ψ, then ψ is valid.


a.	If Δ ⊨ ψ, then Δ ⊭ ¬ψ.
b.	If Δ ⊭ ¬ψ, then Δ ⊨ ψ.
c.	If Δ ⊨ (φ ∨ ψ), then Δ ⊨ φ or Δ ⊨ ψ.
d.	If Γ∪Δ ⊨ φ, then Γ ⊨ φ or Δ ⊨ φ.
e.	If Γ ⊨ φ and Δ ⊨ ψ, then Γ ∩ Δ ⊨ (φ ∧ ψ).

a.	If Δ ⊨ ψ, then Δ ⊭ ¬ψ.
b.	If Δ ⊭ ¬ψ, then Δ ⊨ ψ.
c.	If Γ ⊨ φ and Δ ⊨ ψ, then Γ ∩ Δ ⊨ (φ ∧ ψ).
d.	If φ ⊨ ψ and φ ⊨ ¬ψ, then φ is unsatisfiable.
e.	If φ ⊨ ψ and ¬φ ⊨ ψ, then ψ is valid.

unary
()
¬
unsatisfiable
satisfiable
valid

binary
∩
∪
∧
∨
⊨
⊭
consistent
then

"""
import re

operator_nums = {
    "∩": 10,
    "∪": 9,
    "∧": 8,
    "∨": 7,
    "⊨": 6,
    "⊭": 5,
    "or": 4,
    "and": 3,
    "consistent": 2,
    "then": 1,
}

transform = {
    10: lambda a, b: f"intersect({a}, {b})",
    9: lambda a, b: f"union({a}, {b})",
    8: lambda a, b: f"({a} and {b})",
    7: lambda a, b: f"({a} or {b})",
    6: lambda a, b: f"all(lambda x: implies({a}, {b}))",
    5: lambda a, b: f"(not all(lambda x: implies({a}, {b})))",
    4: lambda a, b: f"({a} or {b})",
    3: lambda a, b: f"({a} and {b})",
    2: lambda a, b: f"some(lambda x: {a} and {b})",
    1: lambda a, b: f"implies({a}, {b})",
}

variables = {
    "Γ": "p(x)",
    "Δ": "q(x)",
    "φ": "r1(x)",
    "ψ": "r2(x)",
}

def get_operator(num):
    for operator, operator_num in operator_nums.items():
        if operator_num == num:
            return operator

    raise ValueError(f"Invalid num {num}")

class EntailsParser:
    def __init__(self):
        self.r_swap_flag = False

    def parse_expr(self, e: str):
        e = e.replace("If ", "")
        e = e.replace("is ", "")
        e = e.replace("are ", "")
        e = e.replace(",", "")
        e = e.replace(".", "")
        e = e.replace("{", "")
        e = e.replace("}", "")
        e = "".join(e.split())

        if not e:
            raise RuntimeError("Unknown proposition")


        if "then" not in e:
            if e.endswith("unsatisfiable"):
                val = self.parse_expr(e[:-13])

                return f"(not satisfiable(lambda x: {val}))"
            elif e.endswith("satisfiable"):
                val = self.parse_expr(e[:-11])

                return f"satisfiable(lambda x: {val})"
            elif e.endswith("valid"):
                val = self.parse_expr(e[:-5])

                return f"valid(lambda x: {val})"

        paren_count = 0
        # (operator num, index)
        splits = list()
        for i, c in enumerate(e):
            if c == "(":
                paren_count += 1
            elif c == ")":
                paren_count -= 1

            if paren_count == 0:
                for operator, operator_num in operator_nums.items():
                    if e[i:].startswith(operator):
                        splits.append((operator_num, i))

        if splits:
            splits.sort()

            operator_num, index = splits[0]

            if operator_num == 2:
                e = e[:index]
                e1, e2 = [variables[c] for c in e if c in variables]
            else:
                operator = get_operator(operator_num)
                l = len(operator)

                e1 = e[:index]
                e2 = e[index + l:]
                e1 = self.parse_expr(e1)
                e2 = self.parse_expr(e2)

            return transform[operator_num](e1, e2)

        if e[0] == "(" and e[-1] == ")":
            return self.parse_expr(e[1:-1])
        elif e[0] == "¬":
            val = self.parse_expr(e[1:])

            return f"(not {val})"
        elif e in variables:
            return variables[e]
        else:
            raise RuntimeError("Invalid expression")

exprs = """
a.	If Γ ⊨ (φ ∨ ψ), then Γ ⊨ φ or Γ ⊨ ψ.
b.	If Γ ⊨ (φ ∧ ψ) and Γ ⊨ (φ ∧ ¬ψ), then Γ ⊨ φ.
c.	If Γ ⊨ (φ ∨ ψ) and Γ ⊨ (φ ∨ ¬ψ), then Γ ⊨ φ.
d.	If φ ⊨ ψ and ¬φ ⊨ ψ, then φ is unsatisfiable.
e.	If φ ⊨ ψ or ψ ⊨ φ, then φ and ψ are consistent
"""

if __name__ == "__main__":
    for expr in exprs.splitlines():
        expr = expr[3:]
        expr = expr.strip()
        if not expr:
            continue

        expr = EntailsParser().parse_expr(expr)
        #print(expr)
        val = check(expr)
        print(val == "Valid")
