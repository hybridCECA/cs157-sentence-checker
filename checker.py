from itertools import chain, combinations

model = None

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


all_false = True
all_true = True
for m in powerset(list(range(16))):
    model = m

    val = some(lambda x: p(x) and not q(x)) == all(lambda x: not p(x) or q(x))
    # val = all(lambda x: implies(p(x), q(x))) == implies(all(lambda x: p(x)), all(lambda x: q(x)))
    # val = implies(all(lambda x: all(lambda y: r(x, y))), not some(lambda x: r(x, x)))
    # val = all(lambda x: all(lambda y: implies(p(x), q(y)))) == implies(some(lambda x: p(x)), all(lambda y: q(y)))
    # val = some(lambda x: p(x)) or not all(lambda x: p(x))

    print(val)

    if val:
        all_false = False
    else:
        all_true = False

print()
if not all_false and not all_true:
    print("Contingent")
if all_false:
    print("Unsatisfiable")
if all_true:
    print("Valid")
