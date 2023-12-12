from itertools import chain, combinations

model = None

def union(a, b):
    return a and b

def intersect(a, b):
    return a or b

def entails(f1, f2):
    return all(lambda x: implies(f1(x), f2(x)))

def satisfiable(f):
    return some(lambda x: f(x))

def valid(f):
    return all(lambda x: f(x))

def implies(a, b):
    return not a or b

def get_bit(n, bit_num):
    n >>= bit_num

    return n & 1

def p(n):
    return get_bit(n, 0) == 1

def q(n):
    return get_bit(n, 1) == 1

def r(x, y):
    return get_bit(x, 2) != get_bit(y, 3)

# r split into 2 functions
# DO NOT USE r and (r1 or r2)
def r1(x):
    return get_bit(x, 2)

def r2(x):
    return get_bit(x, 3)

def all(func):
    is_all = True
    for term in model:
        is_all = is_all and func(term)

    return is_all

def some(func):
    is_any = False
    for term in model:
        is_any = is_any or func(term)

    return is_any


def powerset(iterable):
    s = list(iterable)

    p_set = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

    return p_set[1:]


exprs = """
a.	∃x.(p(x) ∧ ¬q(x)) ⇔ ∀x.(¬p(x) ∨ q(x))	
b.	∀x.(p(x) ⇒ q(x)) ⇔ (∀x.p(x) ⇒ ∀x.q(x))	
c.	∀x.∀y.r(x,y) ⇒ ¬∃x.r(x,x)	
d.	∀x.∀y.(p(x) ⇒ q(y)) ⇔ (∃x.p(x) ⇒ ∀y.q(y))	
e.	∃x.p(x) ∨ ¬∀x.p(x)
"""


def check(expr):
    global model

    all_false = True
    all_true = True
    for m in powerset(list(range(16))):
        model = m

        val = eval(expr)

        if val:
            all_false = False
        else:
            all_true = False

    if not all_false and not all_true:
        return "Contingent"
    if all_false:
        return "Unsatisfiable"
    if all_true:
        return "Valid"

if __name__ == "__main__":
    expr = "implies(not (entails(p, lambda x: not q(x))), entails(p, q))"
    # expr = "some(lambda x: p(x) and not q(x)) == all(lambda x: not p(x) or q(x))"
    # expr = all(lambda x: implies(p(x), q(x))) == implies(all(lambda x: p(x)), all(lambda x: q(x)))
    # expr = implies(all(lambda x: all(lambda y: r(x, y))), not some(lambda x: r(x, x)))
    # expr = all(lambda x: all(lambda y: implies(p(x), q(y)))) == implies(some(lambda x: p(x)), all(lambda y: q(y)))
    # expr = some(lambda x: p(x)) or not all(lambda x: p(x))

    val = check(expr)
    print(val)