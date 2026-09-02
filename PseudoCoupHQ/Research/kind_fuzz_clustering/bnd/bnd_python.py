
import sys, ctypes, math
from decimal import Decimal
from fractions import Fraction

EXACT = {"+", "-", "*", "<", "<=", ">", ">=", "==", "!="}

def want(op, a, b):
    if op not in EXACT: return None
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b,
            "==": a == b, "!=": a != b}[op]

def asnum(r):
    if isinstance(r, bool): return r
    if isinstance(r, int): return Fraction(r)
    if isinstance(r, float):
        if r != r or r in (float("inf"), float("-inf")): return None
        return Fraction(r)
    if isinstance(r, Decimal):
        try: return Fraction(r)
        except Exception: return None
    if isinstance(r, Fraction): return r
    return None

def fid(r, op, a, b):
    w = want(op, a, b)
    if w is None: return "na"
    g = asnum(r)
    if g is None: return "na"
    if isinstance(w, bool) or isinstance(g, bool):
        if not (isinstance(w, bool) and isinstance(g, bool)): return "na"
        return "exact" if w == g else "inexact"
    return "exact" if g == Fraction(w) else "inexact"

def sig(fn, c, op, a, b):
    try:
        r = fn(c)
    except BaseException as e:
        return "raise|%s|na" % type(e).__name__
    return "answer|%s|%s" % (type(r).__name__, fid(r, op, a, b))

def bisect(tid, fn, op, lov, hiv, fixed, vary_is_lhs):
    def s(c):
        a = c if vary_is_lhs else fixed
        b = fixed if vary_is_lhs else c
        return sig(lambda x: fn(x), c, op, Fraction(a), Fraction(b))
    lo, hi = lov, hiv
    slo, shi = s(lo), s(hi)
    probes = 2
    if slo == shi:
        print("N|%d|%s|%s" % (tid, slo, shi)); return probes
    other = set()
    while hi - lo > 1:
        mid = (lo + hi) // 2
        sm = s(mid); probes += 1
        if sm == slo: lo = mid
        else:
            if sm != shi: other.add(sm)
            hi = mid
    print("B|%d|%d|%d|%s|%s|%d|%s" %
          (tid, lo, hi, slo, shi, probes, ";".join(sorted(other))))
    return probes


TARGETS = []
def _t3471():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3471, lambda c: ((c) * (f)), '*', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3471)
def _t3472():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3472, lambda c: ((c) <= (f)), '<=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3472)
def _t3473():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3473, lambda c: ((c) > (f)), '>', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3473)
def _t3474():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3474, lambda c: ((c) == (f)), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3474)
def _t3475():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3475, lambda c: ((c) != (f)), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3475)
def _t3479():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3479, lambda c: ((c) * (f)), '*', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3479)
def _t3480():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3480, lambda c: ((c) < (f)), '<', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3480)
def _t3481():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3481, lambda c: ((c) >= (f)), '>=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3481)
def _t3482():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3482, lambda c: ((c) == (f)), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3482)
def _t3483():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3483, lambda c: ((c) != (f)), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3483)
def _t3750():
    f = 42
    return bisect(3750, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 42, True)
TARGETS.append(_t3750)
def _t3751():
    f = 42
    return bisect(3751, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 42, True)
TARGETS.append(_t3751)
def _t3752():
    f = 0
    return bisect(3752, lambda c: ((Decimal(c)) / (f)), '/', 0, 42, 0, True)
TARGETS.append(_t3752)
def _t3753():
    f = 0
    return bisect(3753, lambda c: ((Decimal(c)) // (f)), '//', 0, 42, 0, True)
TARGETS.append(_t3753)
def _t3755():
    f = 0
    return bisect(3755, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 0, True)
TARGETS.append(_t3755)
def _t3756():
    f = 0
    return bisect(3756, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 0, True)
TARGETS.append(_t3756)
def _t3758():
    f = 9223372036854775807
    return bisect(3758, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 9223372036854775807, True)
TARGETS.append(_t3758)
def _t3759():
    f = 9223372036854775807
    return bisect(3759, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 9223372036854775807, True)
TARGETS.append(_t3759)
def _t3761():
    f = 9223372036854775808
    return bisect(3761, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3761)
def _t3762():
    f = 9223372036854775808
    return bisect(3762, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3762)
def _t3764():
    f = 9007199254740993
    return bisect(3764, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 9007199254740993, True)
TARGETS.append(_t3764)
def _t3765():
    f = 9007199254740993
    return bisect(3765, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 9007199254740993, True)
TARGETS.append(_t3765)
def _t3767():
    f = 18446744073709551615
    return bisect(3767, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3767)
def _t3768():
    f = 18446744073709551615
    return bisect(3768, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3768)
def _t3793():
    f = ctypes.c_int64(42).value
    return bisect(3793, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 42, True)
TARGETS.append(_t3793)
def _t3794():
    f = ctypes.c_int64(42).value
    return bisect(3794, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 42, True)
TARGETS.append(_t3794)
def _t3795():
    f = ctypes.c_int64(0).value
    return bisect(3795, lambda c: ((Decimal(c)) / (f)), '/', 0, 42, 0, True)
TARGETS.append(_t3795)
def _t3796():
    f = ctypes.c_int64(0).value
    return bisect(3796, lambda c: ((Decimal(c)) // (f)), '//', 0, 42, 0, True)
TARGETS.append(_t3796)
def _t3798():
    f = ctypes.c_int64(0).value
    return bisect(3798, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 0, True)
TARGETS.append(_t3798)
def _t3799():
    f = ctypes.c_int64(0).value
    return bisect(3799, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 0, True)
TARGETS.append(_t3799)
def _t3801():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(3801, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 9223372036854775807, True)
TARGETS.append(_t3801)
def _t3802():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(3802, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 9223372036854775807, True)
TARGETS.append(_t3802)
def _t3803():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3803, lambda c: ((Decimal(c)) <= (f)), '<=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3803)
def _t3804():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3804, lambda c: ((Decimal(c)) > (f)), '>', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3804)
def _t3805():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3805, lambda c: ((Decimal(c)) == (f)), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3805)
def _t3806():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3806, lambda c: ((Decimal(c)) != (f)), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t3806)
def _t3807():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3807, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3807)
def _t3808():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(3808, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3808)
def _t3810():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(3810, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 9007199254740993, True)
TARGETS.append(_t3810)
def _t3811():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(3811, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 9007199254740993, True)
TARGETS.append(_t3811)
def _t3812():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3812, lambda c: ((Decimal(c)) < (f)), '<', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3812)
def _t3813():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3813, lambda c: ((Decimal(c)) >= (f)), '>=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3813)
def _t3814():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3814, lambda c: ((Decimal(c)) == (f)), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3814)
def _t3815():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3815, lambda c: ((Decimal(c)) != (f)), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t3815)
def _t3816():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3816, lambda c: ((Decimal(c)) and (f)), 'and', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3816)
def _t3817():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(3817, lambda c: ((Decimal(c)) or (f)), 'or', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3817)
def _t3983():
    f = 42
    return bisect(3983, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 42, True)
TARGETS.append(_t3983)
def _t3984():
    f = 42
    return bisect(3984, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 42, True)
TARGETS.append(_t3984)
def _t3985():
    f = 0
    return bisect(3985, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 0, True)
TARGETS.append(_t3985)
def _t3986():
    f = 0
    return bisect(3986, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 0, True)
TARGETS.append(_t3986)
def _t3988():
    f = 9223372036854775807
    return bisect(3988, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 9223372036854775807, True)
TARGETS.append(_t3988)
def _t3989():
    f = 9223372036854775807
    return bisect(3989, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 9223372036854775807, True)
TARGETS.append(_t3989)
def _t3991():
    f = 9223372036854775808
    return bisect(3991, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3991)
def _t3992():
    f = 9223372036854775808
    return bisect(3992, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 9223372036854775808, True)
TARGETS.append(_t3992)
def _t3994():
    f = 9007199254740993
    return bisect(3994, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 9007199254740993, True)
TARGETS.append(_t3994)
def _t3995():
    f = 9007199254740993
    return bisect(3995, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 9007199254740993, True)
TARGETS.append(_t3995)
def _t3997():
    f = 18446744073709551615
    return bisect(3997, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3997)
def _t3998():
    f = 18446744073709551615
    return bisect(3998, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 18446744073709551615, True)
TARGETS.append(_t3998)
def _t4015():
    f = ctypes.c_int64(42).value
    return bisect(4015, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 42, True)
TARGETS.append(_t4015)
def _t4016():
    f = ctypes.c_int64(42).value
    return bisect(4016, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 42, True)
TARGETS.append(_t4016)
def _t4017():
    f = ctypes.c_int64(0).value
    return bisect(4017, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 0, True)
TARGETS.append(_t4017)
def _t4018():
    f = ctypes.c_int64(0).value
    return bisect(4018, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 0, True)
TARGETS.append(_t4018)
def _t4020():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4020, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 9223372036854775807, True)
TARGETS.append(_t4020)
def _t4021():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4021, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 9223372036854775807, True)
TARGETS.append(_t4021)
def _t4022():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4022, lambda c: ((Fraction(c)) <= (f)), '<=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4022)
def _t4023():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4023, lambda c: ((Fraction(c)) > (f)), '>', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4023)
def _t4024():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4024, lambda c: ((Fraction(c)) == (f)), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4024)
def _t4025():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4025, lambda c: ((Fraction(c)) != (f)), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4025)
def _t4027():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4027, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 9223372036854775808, True)
TARGETS.append(_t4027)
def _t4028():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4028, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 9223372036854775808, True)
TARGETS.append(_t4028)
def _t4030():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4030, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 9007199254740993, True)
TARGETS.append(_t4030)
def _t4031():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4031, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 9007199254740993, True)
TARGETS.append(_t4031)
def _t4032():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4032, lambda c: ((Fraction(c)) < (f)), '<', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4032)
def _t4033():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4033, lambda c: ((Fraction(c)) >= (f)), '>=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4033)
def _t4034():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4034, lambda c: ((Fraction(c)) == (f)), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4034)
def _t4035():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4035, lambda c: ((Fraction(c)) != (f)), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4035)
def _t4037():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4037, lambda c: ((Fraction(c)) and (f)), 'and', 0, 42, 18446744073709551615, True)
TARGETS.append(_t4037)
def _t4038():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4038, lambda c: ((Fraction(c)) or (f)), 'or', 0, 42, 18446744073709551615, True)
TARGETS.append(_t4038)
def _t4222():
    f = 9223372036854775808
    return bisect(4222, lambda c: ((ctypes.c_int64(c).value) <= (f)), '<=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4222)
def _t4223():
    f = 9223372036854775808
    return bisect(4223, lambda c: ((ctypes.c_int64(c).value) > (f)), '>', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4223)
def _t4224():
    f = 9223372036854775808
    return bisect(4224, lambda c: ((ctypes.c_int64(c).value) == (f)), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4224)
def _t4225():
    f = 9223372036854775808
    return bisect(4225, lambda c: ((ctypes.c_int64(c).value) != (f)), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4225)
def _t4232():
    f = 18446744073709551615
    return bisect(4232, lambda c: ((ctypes.c_int64(c).value) < (f)), '<', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4232)
def _t4233():
    f = 18446744073709551615
    return bisect(4233, lambda c: ((ctypes.c_int64(c).value) >= (f)), '>=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4233)
def _t4234():
    f = 18446744073709551615
    return bisect(4234, lambda c: ((ctypes.c_int64(c).value) == (f)), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4234)
def _t4235():
    f = 18446744073709551615
    return bisect(4235, lambda c: ((ctypes.c_int64(c).value) != (f)), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, True)
TARGETS.append(_t4235)
def _t4301():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4301, lambda c: ((ctypes.c_int64(c).value) * (f)), '*', 0, 42, 9223372036854775808, True)
TARGETS.append(_t4301)
def _t4302():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4302, lambda c: ((ctypes.c_int64(c).value) * (f)), '*', 9223372036854775808, 18446744073709551615, 9223372036854775808, True)
TARGETS.append(_t4302)
def _t4307():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4307, lambda c: ((ctypes.c_int64(c).value) * (f)), '*', 0, 42, 18446744073709551615, True)
TARGETS.append(_t4307)
def _t4587():
    f = 42
    return bisect(4587, lambda c: ((f) / (c)), '/', 0, 42, 42, False)
TARGETS.append(_t4587)
def _t4588():
    f = 42
    return bisect(4588, lambda c: ((f) % (c)), '%', 0, 42, 42, False)
TARGETS.append(_t4588)
def _t4590():
    f = 42
    return bisect(4590, lambda c: ((f) // (c)), '//', 0, 42, 42, False)
TARGETS.append(_t4590)
def _t4592():
    f = 0
    return bisect(4592, lambda c: ((f) / (c)), '/', 0, 42, 0, False)
TARGETS.append(_t4592)
def _t4593():
    f = 0
    return bisect(4593, lambda c: ((f) % (c)), '%', 0, 42, 0, False)
TARGETS.append(_t4593)
def _t4594():
    f = 0
    return bisect(4594, lambda c: ((f) // (c)), '//', 0, 42, 0, False)
TARGETS.append(_t4594)
def _t4595():
    f = 9223372036854775807
    return bisect(4595, lambda c: ((f) / (c)), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4595)
def _t4596():
    f = 9223372036854775807
    return bisect(4596, lambda c: ((f) % (c)), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4596)
def _t4598():
    f = 9223372036854775807
    return bisect(4598, lambda c: ((f) // (c)), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4598)
def _t4600():
    f = 9223372036854775808
    return bisect(4600, lambda c: ((f) / (c)), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4600)
def _t4601():
    f = 9223372036854775808
    return bisect(4601, lambda c: ((f) % (c)), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4601)
def _t4603():
    f = 9223372036854775808
    return bisect(4603, lambda c: ((f) // (c)), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4603)
def _t4605():
    f = 9007199254740993
    return bisect(4605, lambda c: ((f) / (c)), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4605)
def _t4606():
    f = 9007199254740993
    return bisect(4606, lambda c: ((f) % (c)), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4606)
def _t4608():
    f = 9007199254740993
    return bisect(4608, lambda c: ((f) // (c)), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4608)
def _t4610():
    f = 18446744073709551615
    return bisect(4610, lambda c: ((f) / (c)), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4610)
def _t4611():
    f = 18446744073709551615
    return bisect(4611, lambda c: ((f) % (c)), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4611)
def _t4613():
    f = 18446744073709551615
    return bisect(4613, lambda c: ((f) // (c)), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4613)
def _t4615():
    f = 42
    return bisect(4615, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 42, False)
TARGETS.append(_t4615)
def _t4616():
    f = 42
    return bisect(4616, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 42, False)
TARGETS.append(_t4616)
def _t4617():
    f = 42
    return bisect(4617, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 42, False)
TARGETS.append(_t4617)
def _t4619():
    f = 0
    return bisect(4619, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 0, False)
TARGETS.append(_t4619)
def _t4620():
    f = 0
    return bisect(4620, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 0, False)
TARGETS.append(_t4620)
def _t4621():
    f = 0
    return bisect(4621, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 0, False)
TARGETS.append(_t4621)
def _t4623():
    f = 9223372036854775807
    return bisect(4623, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4623)
def _t4624():
    f = 9223372036854775807
    return bisect(4624, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4624)
def _t4625():
    f = 9223372036854775807
    return bisect(4625, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4625)
def _t4627():
    f = 9223372036854775808
    return bisect(4627, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4627)
def _t4628():
    f = 9223372036854775808
    return bisect(4628, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4628)
def _t4629():
    f = 9223372036854775808
    return bisect(4629, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4629)
def _t4631():
    f = 9007199254740993
    return bisect(4631, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4631)
def _t4632():
    f = 9007199254740993
    return bisect(4632, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4632)
def _t4633():
    f = 9007199254740993
    return bisect(4633, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4633)
def _t4635():
    f = 18446744073709551615
    return bisect(4635, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4635)
def _t4636():
    f = 18446744073709551615
    return bisect(4636, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4636)
def _t4637():
    f = 18446744073709551615
    return bisect(4637, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4637)
def _t4639():
    f = 42
    return bisect(4639, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 42, False)
TARGETS.append(_t4639)
def _t4640():
    f = 42
    return bisect(4640, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 42, False)
TARGETS.append(_t4640)
def _t4641():
    f = 42
    return bisect(4641, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 42, False)
TARGETS.append(_t4641)
def _t4643():
    f = 0
    return bisect(4643, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 0, False)
TARGETS.append(_t4643)
def _t4644():
    f = 0
    return bisect(4644, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 0, False)
TARGETS.append(_t4644)
def _t4645():
    f = 0
    return bisect(4645, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 0, False)
TARGETS.append(_t4645)
def _t4646():
    f = 9223372036854775807
    return bisect(4646, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4646)
def _t4647():
    f = 9223372036854775807
    return bisect(4647, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4647)
def _t4648():
    f = 9223372036854775807
    return bisect(4648, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4648)
def _t4650():
    f = 9223372036854775808
    return bisect(4650, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4650)
def _t4651():
    f = 9223372036854775808
    return bisect(4651, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4651)
def _t4652():
    f = 9223372036854775808
    return bisect(4652, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4652)
def _t4654():
    f = 9007199254740993
    return bisect(4654, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4654)
def _t4655():
    f = 9007199254740993
    return bisect(4655, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4655)
def _t4656():
    f = 9007199254740993
    return bisect(4656, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4656)
def _t4658():
    f = 18446744073709551615
    return bisect(4658, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4658)
def _t4659():
    f = 18446744073709551615
    return bisect(4659, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4659)
def _t4660():
    f = 18446744073709551615
    return bisect(4660, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4660)
def _t4662():
    f = 42
    return bisect(4662, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 42, False)
TARGETS.append(_t4662)
def _t4663():
    f = 42
    return bisect(4663, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 42, False)
TARGETS.append(_t4663)
def _t4665():
    f = 42
    return bisect(4665, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 42, False)
TARGETS.append(_t4665)
def _t4667():
    f = 0
    return bisect(4667, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 0, False)
TARGETS.append(_t4667)
def _t4668():
    f = 0
    return bisect(4668, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 0, False)
TARGETS.append(_t4668)
def _t4669():
    f = 0
    return bisect(4669, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 0, False)
TARGETS.append(_t4669)
def _t4670():
    f = 9223372036854775807
    return bisect(4670, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4670)
def _t4671():
    f = 9223372036854775807
    return bisect(4671, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4671)
def _t4673():
    f = 9223372036854775807
    return bisect(4673, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4673)
def _t4675():
    f = 9223372036854775808
    return bisect(4675, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4675)
def _t4676():
    f = 9223372036854775808
    return bisect(4676, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4676)
def _t4677():
    f = 9223372036854775808
    return bisect(4677, lambda c: ((f) < (ctypes.c_int64(c).value)), '<', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4677)
def _t4678():
    f = 9223372036854775808
    return bisect(4678, lambda c: ((f) >= (ctypes.c_int64(c).value)), '>=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4678)
def _t4679():
    f = 9223372036854775808
    return bisect(4679, lambda c: ((f) == (ctypes.c_int64(c).value)), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4679)
def _t4680():
    f = 9223372036854775808
    return bisect(4680, lambda c: ((f) != (ctypes.c_int64(c).value)), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4680)
def _t4682():
    f = 9223372036854775808
    return bisect(4682, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4682)
def _t4684():
    f = 9007199254740993
    return bisect(4684, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4684)
def _t4685():
    f = 9007199254740993
    return bisect(4685, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4685)
def _t4687():
    f = 9007199254740993
    return bisect(4687, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4687)
def _t4689():
    f = 18446744073709551615
    return bisect(4689, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4689)
def _t4690():
    f = 18446744073709551615
    return bisect(4690, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4690)
def _t4691():
    f = 18446744073709551615
    return bisect(4691, lambda c: ((f) <= (ctypes.c_int64(c).value)), '<=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4691)
def _t4692():
    f = 18446744073709551615
    return bisect(4692, lambda c: ((f) > (ctypes.c_int64(c).value)), '>', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4692)
def _t4693():
    f = 18446744073709551615
    return bisect(4693, lambda c: ((f) == (ctypes.c_int64(c).value)), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4693)
def _t4694():
    f = 18446744073709551615
    return bisect(4694, lambda c: ((f) != (ctypes.c_int64(c).value)), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4694)
def _t4696():
    f = 18446744073709551615
    return bisect(4696, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4696)
def _t4866():
    f = ctypes.c_int64(42).value
    return bisect(4866, lambda c: ((f) / (c)), '/', 0, 42, 42, False)
TARGETS.append(_t4866)
def _t4867():
    f = ctypes.c_int64(42).value
    return bisect(4867, lambda c: ((f) % (c)), '%', 0, 42, 42, False)
TARGETS.append(_t4867)
def _t4869():
    f = ctypes.c_int64(42).value
    return bisect(4869, lambda c: ((f) // (c)), '//', 0, 42, 42, False)
TARGETS.append(_t4869)
def _t4871():
    f = ctypes.c_int64(0).value
    return bisect(4871, lambda c: ((f) / (c)), '/', 0, 42, 0, False)
TARGETS.append(_t4871)
def _t4872():
    f = ctypes.c_int64(0).value
    return bisect(4872, lambda c: ((f) % (c)), '%', 0, 42, 0, False)
TARGETS.append(_t4872)
def _t4873():
    f = ctypes.c_int64(0).value
    return bisect(4873, lambda c: ((f) // (c)), '//', 0, 42, 0, False)
TARGETS.append(_t4873)
def _t4874():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4874, lambda c: ((f) / (c)), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4874)
def _t4875():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4875, lambda c: ((f) % (c)), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4875)
def _t4877():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4877, lambda c: ((f) // (c)), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4877)
def _t4879():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4879, lambda c: ((f) * (c)), '*', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4879)
def _t4880():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4880, lambda c: ((f) / (c)), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4880)
def _t4881():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4881, lambda c: ((f) % (c)), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4881)
def _t4882():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4882, lambda c: ((f) < (c)), '<', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4882)
def _t4883():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4883, lambda c: ((f) >= (c)), '>=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4883)
def _t4884():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4884, lambda c: ((f) == (c)), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4884)
def _t4885():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4885, lambda c: ((f) != (c)), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4885)
def _t4887():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4887, lambda c: ((f) // (c)), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4887)
def _t4889():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4889, lambda c: ((f) / (c)), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4889)
def _t4890():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4890, lambda c: ((f) % (c)), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4890)
def _t4892():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4892, lambda c: ((f) // (c)), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4892)
def _t4894():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4894, lambda c: ((f) * (c)), '*', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4894)
def _t4895():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4895, lambda c: ((f) / (c)), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4895)
def _t4896():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4896, lambda c: ((f) % (c)), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4896)
def _t4897():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4897, lambda c: ((f) <= (c)), '<=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4897)
def _t4898():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4898, lambda c: ((f) > (c)), '>', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4898)
def _t4899():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4899, lambda c: ((f) == (c)), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4899)
def _t4900():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4900, lambda c: ((f) != (c)), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4900)
def _t4902():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4902, lambda c: ((f) // (c)), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4902)
def _t4903():
    f = ctypes.c_int64(42).value
    return bisect(4903, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 42, False)
TARGETS.append(_t4903)
def _t4904():
    f = ctypes.c_int64(42).value
    return bisect(4904, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 42, False)
TARGETS.append(_t4904)
def _t4905():
    f = ctypes.c_int64(42).value
    return bisect(4905, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 42, False)
TARGETS.append(_t4905)
def _t4907():
    f = ctypes.c_int64(0).value
    return bisect(4907, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 0, False)
TARGETS.append(_t4907)
def _t4908():
    f = ctypes.c_int64(0).value
    return bisect(4908, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 0, False)
TARGETS.append(_t4908)
def _t4909():
    f = ctypes.c_int64(0).value
    return bisect(4909, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 0, False)
TARGETS.append(_t4909)
def _t4911():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4911, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4911)
def _t4912():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4912, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4912)
def _t4913():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4913, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4913)
def _t4915():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4915, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4915)
def _t4916():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4916, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4916)
def _t4917():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4917, lambda c: ((f) < (Decimal(c))), '<', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4917)
def _t4918():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4918, lambda c: ((f) >= (Decimal(c))), '>=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4918)
def _t4919():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4919, lambda c: ((f) == (Decimal(c))), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4919)
def _t4920():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4920, lambda c: ((f) != (Decimal(c))), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4920)
def _t4921():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4921, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4921)
def _t4923():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4923, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4923)
def _t4924():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4924, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4924)
def _t4925():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4925, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4925)
def _t4927():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4927, lambda c: ((f) / (Decimal(c))), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4927)
def _t4928():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4928, lambda c: ((f) % (Decimal(c))), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4928)
def _t4929():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4929, lambda c: ((f) <= (Decimal(c))), '<=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4929)
def _t4930():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4930, lambda c: ((f) > (Decimal(c))), '>', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4930)
def _t4931():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4931, lambda c: ((f) == (Decimal(c))), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4931)
def _t4932():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4932, lambda c: ((f) != (Decimal(c))), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4932)
def _t4933():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4933, lambda c: ((f) // (Decimal(c))), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4933)
def _t4934():
    f = ctypes.c_int64(42).value
    return bisect(4934, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 42, False)
TARGETS.append(_t4934)
def _t4935():
    f = ctypes.c_int64(42).value
    return bisect(4935, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 42, False)
TARGETS.append(_t4935)
def _t4936():
    f = ctypes.c_int64(42).value
    return bisect(4936, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 42, False)
TARGETS.append(_t4936)
def _t4938():
    f = ctypes.c_int64(0).value
    return bisect(4938, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 0, False)
TARGETS.append(_t4938)
def _t4939():
    f = ctypes.c_int64(0).value
    return bisect(4939, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 0, False)
TARGETS.append(_t4939)
def _t4940():
    f = ctypes.c_int64(0).value
    return bisect(4940, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 0, False)
TARGETS.append(_t4940)
def _t4941():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4941, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4941)
def _t4942():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4942, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4942)
def _t4943():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4943, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4943)
def _t4945():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4945, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4945)
def _t4946():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4946, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4946)
def _t4947():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4947, lambda c: ((f) < (Fraction(c))), '<', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4947)
def _t4948():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4948, lambda c: ((f) >= (Fraction(c))), '>=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4948)
def _t4949():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4949, lambda c: ((f) == (Fraction(c))), '==', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4949)
def _t4950():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4950, lambda c: ((f) != (Fraction(c))), '!=', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4950)
def _t4951():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4951, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4951)
def _t4953():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4953, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4953)
def _t4954():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4954, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4954)
def _t4955():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4955, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4955)
def _t4957():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4957, lambda c: ((f) / (Fraction(c))), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4957)
def _t4958():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4958, lambda c: ((f) % (Fraction(c))), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4958)
def _t4959():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4959, lambda c: ((f) <= (Fraction(c))), '<=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4959)
def _t4960():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4960, lambda c: ((f) > (Fraction(c))), '>', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4960)
def _t4961():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4961, lambda c: ((f) == (Fraction(c))), '==', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4961)
def _t4962():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4962, lambda c: ((f) != (Fraction(c))), '!=', 9223372036854775808, 18446744073709551615, 18446744073709551615, False)
TARGETS.append(_t4962)
def _t4963():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4963, lambda c: ((f) // (Fraction(c))), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4963)
def _t4964():
    f = ctypes.c_int64(42).value
    return bisect(4964, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 42, False)
TARGETS.append(_t4964)
def _t4965():
    f = ctypes.c_int64(42).value
    return bisect(4965, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 42, False)
TARGETS.append(_t4965)
def _t4967():
    f = ctypes.c_int64(42).value
    return bisect(4967, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 42, False)
TARGETS.append(_t4967)
def _t4969():
    f = ctypes.c_int64(0).value
    return bisect(4969, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 0, False)
TARGETS.append(_t4969)
def _t4970():
    f = ctypes.c_int64(0).value
    return bisect(4970, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 0, False)
TARGETS.append(_t4970)
def _t4971():
    f = ctypes.c_int64(0).value
    return bisect(4971, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 0, False)
TARGETS.append(_t4971)
def _t4972():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4972, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4972)
def _t4973():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4973, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4973)
def _t4975():
    f = ctypes.c_int64(9223372036854775807).value
    return bisect(4975, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 9223372036854775807, False)
TARGETS.append(_t4975)
def _t4977():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4977, lambda c: ((f) * (ctypes.c_int64(c).value)), '*', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4977)
def _t4978():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4978, lambda c: ((f) * (ctypes.c_int64(c).value)), '*', 9223372036854775808, 18446744073709551615, 9223372036854775808, False)
TARGETS.append(_t4978)
def _t4979():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4979, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4979)
def _t4980():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4980, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4980)
def _t4982():
    f = ctypes.c_int64(9223372036854775808).value
    return bisect(4982, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 9223372036854775808, False)
TARGETS.append(_t4982)
def _t4984():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4984, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 9007199254740993, False)
TARGETS.append(_t4984)
def _t4985():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4985, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 9007199254740993, False)
TARGETS.append(_t4985)
def _t4987():
    f = ctypes.c_int64(9007199254740993).value
    return bisect(4987, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 9007199254740993, False)
TARGETS.append(_t4987)
def _t4989():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4989, lambda c: ((f) * (ctypes.c_int64(c).value)), '*', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4989)
def _t4990():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4990, lambda c: ((f) / (ctypes.c_int64(c).value)), '/', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4990)
def _t4991():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4991, lambda c: ((f) % (ctypes.c_int64(c).value)), '%', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4991)
def _t4993():
    f = ctypes.c_int64(18446744073709551615).value
    return bisect(4993, lambda c: ((f) // (ctypes.c_int64(c).value)), '//', 0, 42, 18446744073709551615, False)
TARGETS.append(_t4993)
def main():
    total = 0
    n = len(TARGETS)
    for k, t in enumerate(TARGETS):
        total += t()
        if (k + 1) % 25 == 0 or k + 1 == n:
            sys.stderr.write("progress %d/%d probes=%d\n" % (k + 1, n, total))
            sys.stderr.flush()
    sys.stderr.write("DONE targets=%d probes=%d\n" % (n, total))

main()
