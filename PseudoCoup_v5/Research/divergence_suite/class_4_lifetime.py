"""Class 4 — lifetime / observation.

Naive divergence: WHEN cleanup runs.
  C++ RAII / CPython refcount: deterministic, at scope exit.
  Java/Go/C#/Dart GC finalizers: nondeterministic, possibly never.
A destructor that prints, releases a lock, or flushes a file makes the
divergence observable in output.

Policy fix (policy 6): no effectful destructors; cleanup is an
explicit scope (with / try-finally), which every target has and every
target runs at the same moment.
"""

log = []


class Resource:
    def __init__(self, name: str):
        self.name = name
        log.append("open " + name)

    def close(self) -> None:
        log.append("close " + self.name)

    # canonical scope protocol:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


# canonical: explicit scope. cleanup point identical on all targets.
with Resource("a") as r1:
    with Resource("b") as r2:
        log.append("work")

print(log)   # ['open a', 'open b', 'work', 'close b', 'close a']
# note reverse close order — also pinned by the explicit scoping.
