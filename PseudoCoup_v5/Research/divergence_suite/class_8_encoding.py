"""Class 8 — encoding.

Naive divergence: the unit of string length/indexing.
  s = "h🙂i"
  Python:      len 3, s[1] = 🙂        (code points)
  Java/Dart/JS/C#: length 4, s[1] = broken surrogate half (UTF-16)
  C/PHP bytes: length 6                 (UTF-8 bytes)

Policy fix (policy 5 + Table 3 P7): PC.string = view model (Swift
canon). No unqualified len/[] on strings; every access names its view.
"""

s = "h\U0001F642i"          # h 🙂 i


def view_points(s: str) -> list:
    return list(s)                       # code points (hub-native)


def view_utf8(s: str) -> bytes:
    return s.encode("utf-8")


def view_utf16_units(s: str) -> list:
    b = s.encode("utf-16-le")
    return [b[i] + 256 * b[i + 1] for i in range(0, len(b), 2)]


print("points  len =", len(view_points(s)), " [1] =", view_points(s)[1])
print("utf8    len =", len(view_utf8(s)))
print("utf16   len =", len(view_utf16_units(s)))
# every target computes ALL THREE identically, because each view is
# an explicit computation over PC.bytes — no default unit exists.
