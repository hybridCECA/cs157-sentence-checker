from parser import Parser
from checker import check

if __name__ == "__main__":
    exprs = """
a.	∀x.(p(x) ⇒ q(x)) ⇒ ∃x.(p(x) ∧ q(x))	
b.	∀x.(p(x) ∨ q(x)) ∧ ∀x.(p(x) ⇒ q(x)) ∧ ∃x.¬q(x)	
c.	(∀x.p(x) ⇒ ∀x.q(x)) ∨ (¬∀x.q(x) ⇒ ¬∀x.p(x))	
d.	(∀x.p(x) ⇒ ∃x.q(x)) ∨ (¬∀x.p(x) ⇒ ¬∃x.q(x))	
e.	∀x.∀y.(r(x,y) ⇔ r(y,x)) ⇒ ∃x.r(x,x)
    """

    for expr in exprs.splitlines():
        if not expr.strip():
            continue

        if expr[0].isalpha() and expr[1] == ".":
            expr = expr[2:]

        expr = Parser().parse_expr(expr)

        val = check(expr)
        print(val)