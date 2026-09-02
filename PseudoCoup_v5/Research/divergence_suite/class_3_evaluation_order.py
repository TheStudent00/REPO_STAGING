"""Class 3 — evaluation-order.

Naive divergence: f(g(), h()) — argument evaluation order.
  Python/Java/JS: left-to-right, g then h.
  C++ (pre-17): unspecified; either order legal.
Observable only when arguments have side effects.

Policy fix (policy 6): left-to-right is canonical; egress emits
explicit temporaries so even order-free targets are pinned:
  t1 = g(); t2 = h(); f(t1, t2)
"""

log = []


def g() -> int:
    log.append("g")
    return 1


def h() -> int:
    log.append("h")
    return 2


def f(a: int, b: int) -> int:
    return a + b


# canonical form — and literally what egress emits everywhere:
t1 = g()
t2 = h()
result = f(t1, t2)

print("order  =", log)        # ['g', 'h'] on every target
print("result =", result)
