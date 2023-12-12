from parser import Parser
from checker import check

if __name__ == "__main__":
    exprs = """
a.	∃x.(p(x) ∧ ¬q(x)) ⇔ ∀x.(¬p(x) ∨ q(x))	
b.	∀x.(p(x) ⇒ q(x)) ⇔ (∀x.p(x) ⇒ ∀x.q(x))	
c.	∀x.∀y.r(x,y) ⇒ ¬∃x.r(x,x)	
d.	∀x.∀y.(p(x) ⇒ q(y)) ⇔ (∃x.p(x) ⇒ ∀y.q(y))	
e.	∃x.p(x) ∨ ¬∀x.p(x)
    """

    for expr in exprs.splitlines():
        if not expr.strip():
            continue

        if expr[0].isalpha() and expr[1] == ".":
            expr = expr[2:]

        expr = Parser().parse_expr(expr)

        val = check(expr)
        print(val)