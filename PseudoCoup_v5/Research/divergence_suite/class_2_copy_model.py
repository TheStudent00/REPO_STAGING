"""Class 2 — copy-model.

Naive divergence: identical-looking assignment
  a = b; b.x = 1; print(a.x)
  reference targets (Python/Java/Dart/JS): 1  — a and b alias
  value targets (Go struct, C++ struct, Swift struct): 0 — a is a copy

Policy fix (policy 6): PC.record = reference semantics everywhere;
copying only by explicit .copy() spelling. Value-struct behavior is a
qualified borrow (go.struct), never the unqualified default.
"""


class P:
    def __init__(self, x: int):
        self.x = x

    def copy(self) -> "P":
        return P(self.x)


b = P(0)
a = b            # canonical: alias, on every target
b.x = 1
print("alias  a.x =", a.x)     # 1 everywhere under PC.record

b2 = P(0)
a2 = b2.copy()   # explicit copy: the only way to get value behavior
b2.x = 1
print("copy   a2.x =", a2.x)   # 0 everywhere
