"""Class 5 — dispatch.

Naive divergence: which function a call selects.
  Java/C++ overloads: chosen by the DECLARED type of the argument,
  at compile-time. describe(Animal a) runs even if a holds a Cat.
  Python/Ruby: no overloads; run-time type decides everything.
So identical-looking code selects different functions.

Policy fix (policies 6, 13): no static overloading in the canon.
One function name, one signature; variation by run-time type goes
through single dynamic dispatch (the type->function map). Overload
sets are a qualified borrow (java.overload) if ever admitted.
"""

log = []


class Animal:
    def kind(self) -> str:
        return "animal"


class Cat(Animal):
    def kind(self) -> str:
        return "cat"


def describe(a: Animal) -> str:
    return a.kind()          # canonical: run-time type decides


x: Animal = Cat()            # declared Animal, holds Cat
print("describe(x) =", describe(x))
# 'cat' on every target under the canon.
# naive Java-overload egress would print 'animal' — the divergence.
