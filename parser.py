"""
a.  ∃x.(p(x) ∧ ¬q(x)) ⇔ ∀x.(¬p(x) ∨ q(x))
b.	∀x.(p(x) ⇒ q(x)) ⇔ (∀x.p(x) ⇒ ∀x.q(x))
c.	∀x.∀y.r(x,y) ⇒ ¬∃x.r(x,x)
d.	∀x.∀y.(p(x) ⇒ q(y)) ⇔ (∃x.p(x) ⇒ ∀y.q(y))
e.	∃x.p(x) ∨ ¬∀x.p(x)

# val = some(lambda x: p(x) and not q(x)) == all(lambda x: not p(x) or q(x))
# val = all(lambda x: implies(p(x), q(x))) == implies(all(lambda x: p(x)), all(lambda x: q(x)))
# val = implies(all(lambda x: all(lambda y: r(x, y))), not some(lambda x: r(x, x)))
# val = all(lambda x: all(lambda y: implies(p(x), q(y)))) == implies(some(lambda x: p(x)), all(lambda y: q(y)))
# val = some(lambda x: p(x)) or not all(lambda x: p(x))

()
∀[a-z].e
∃[a-z].e
¬
∧
∨
⇒
⇔
[a-z]([a-z], [a-z])
"""
import re

operator_nums = {
    "∧": 4,
    "∨": 3,
    "⇒": 2,
    "⇔": 1,
}

transform = {
    4: lambda a, b: f"({a} and {b})",
    3: lambda a, b: f"({a} or {b})",
    2: lambda a, b: f"implies({a}, {b})",
    1: lambda a, b: f"({a} == {b})",
}

class Parser:
    def __init__(self):
        self.r_swap_flag = False

    def parse_expr(self, e: str):
        e = "".join(e.split())

        if not e:
            raise RuntimeError("Unknown proposition")

        paren_count = 0
        # (operator num, index)
        splits = list()
        for i, c in enumerate(e):
            if c == "(":
                paren_count += 1
            elif c == ")":
                paren_count -= 1

            if paren_count == 0 and c in operator_nums:
                splits.append((operator_nums[c], i))

        if splits:
            splits.sort()

            operator_num, index = splits[0]

            e1 = e[:index]
            e2 = e[index + 1:]
            e1 = self.parse_expr(e1)
            e2 = self.parse_expr(e2)

            return transform[operator_num](e1, e2)

        if e[0] == "(" and e[-1] == ")":
            return self.parse_expr(e[1:-1])
        elif e[0] == "∀" and e[1].isalpha():
            val = self.parse_expr(e[3:])

            return f"all(lambda {e[1]}: {val})"
        elif e[0] == "∃" and e[1].isalpha():
            val = self.parse_expr(e[3:])

            return f"some(lambda {e[1]}: {val})"
        elif e[0] == "¬":
            val = self.parse_expr(e[1:])

            return f"(not {val})"
        elif re.fullmatch(r"[a-z]\([a-z,]+\)", e):
            if e[0] not in "pqr":
                raise RuntimeError("")

            if "," in e:
                self.r_swap_flag = True

                return "r" + e[1:]
            elif self.r_swap_flag and e[0] == "r":
                raise RuntimeError("Swap flag trip")

            return e
        else:
            raise RuntimeError("Invalid expression")