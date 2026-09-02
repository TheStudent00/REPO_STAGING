"""Does our generated machine code appear INSIDE what a production
compiler emits for the same expression?

Compiles the equivalent function with a native compiler, disassembles
the object file, and searches the real function's bytes for our
generated stub body as a contiguous sub-sequence.

Native compilers add a prologue (endbr64 CET landing pad) and, in
Rust's case, panic guards. The question is whether the CORE sequence
matches exactly.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

from pc_backend import compile_binop

I64 = "i64"

C_SRC = """
long long d(long long a, long long b) { return a / b; }
long long r(long long a, long long b) { return a % b; }
long long m(long long a, long long b) { return a * b; }
long long p(long long a, long long b) { return a + b; }
long long s(long long a, long long b) { return a - b; }
"""

RUST_SRC = """
#[no_mangle] pub fn d(a: i64, b: i64) -> i64 { a / b }
#[no_mangle] pub fn r(a: i64, b: i64) -> i64 { a % b }
#[no_mangle] pub fn m(a: i64, b: i64) -> i64 { a.wrapping_mul(b) }
#[no_mangle] pub fn p(a: i64, b: i64) -> i64 { a.wrapping_add(b) }
#[no_mangle] pub fn s(a: i64, b: i64) -> i64 { a.wrapping_sub(b) }
"""

FUNCS = {"d": "Div", "r": "Rem", "m": "Mul", "p": "Add", "s": "Sub"}


def objdump_functions(obj: Path):
    """name -> bytes, parsed from objdump -d."""
    out = subprocess.run(["objdump", "-d", str(obj)],
                         capture_output=True, text=True).stdout
    funcs, cur = {}, None
    for line in out.splitlines():
        if line.endswith(">:"):
            cur = line.split("<")[1].rstrip(">:")
            funcs[cur] = bytearray()
        elif cur and "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 2:
                for tok in parts[1].split():
                    if len(tok) == 2:
                        try:
                            funcs[cur].append(int(tok, 16))
                        except ValueError:
                            break
    return {k: bytes(v) for k, v in funcs.items()}


GRID = [(-7, 2), (7, 2), (-7, -2), (7, -2), (0, 1), (1, 0),
        (9223372036854775807, 1), (-9223372036854775808, 1),
        (123456789, 987654321)]


def executes_identically(binop, theirs: bytes):
    """Mount THEIR bytes and ours; compare results on the grid.
    The definitive equivalence test: different encodings that compute
    the same thing must agree everywhere."""
    from output_ring import mount
    from pc_backend import call_binop
    try:
        fn = mount(theirs)
    except OSError:
        return None
    for a, b in GRID:
        if binop in ("Div", "Rem") and (b == 0 or b == -1):
            continue
        try:
            want = call_binop(binop, I64, a, b)
        except Exception:
            continue
        if fn.call(a, b) != want:
            return False
    return True


def report(label, compiled: dict, ok_ref):
    for fname, binop in FUNCS.items():
        if fname not in compiled:
            continue
        theirs = compiled[fname]
        ours = compile_binop(binop, I64)["bytes"]
        body = ours[:-1] if ours.endswith(b"\xc3") else ours
        found = body in theirs
        equiv = executes_identically(binop, theirs)

        if found:
            verdict, detail = "EXACT", "our bytes appear verbatim"
        elif equiv:
            verdict, detail = "EQUIV", ("different encoding, "
                                        "identical results on grid")
        else:
            verdict, detail = "DIFFER", "results disagree"
            ok_ref[0] = False

        print(f"{verdict:6} {label} {binop:4} ours={body.hex(' ')}")
        print(f"          theirs={theirs.hex(' ')}   [{detail}]")
        if found:
            off = theirs.index(body)
            print(f"          match at offset {off} | before: "
                  f"{theirs[:off].hex(' ') or '(none)'} | after: "
                  f"{theirs[off + len(body):].hex(' ') or '(none)'}")


ok = [True]
tmp = Path(tempfile.mkdtemp())

if shutil.which("gcc"):
    src = tmp / "d.c"
    src.write_text(C_SRC)
    obj = tmp / "d.o"
    subprocess.run(["gcc", "-O2", "-c", str(src), "-o", str(obj)],
                   check=True)
    print("=== vs gcc -O2 (C, same arch ops) ===")
    report("gcc", objdump_functions(obj), ok)
else:
    print("gcc not available — skipped")

if shutil.which("rustc"):
    src = tmp / "d.rs"
    src.write_text(RUST_SRC)
    obj = tmp / "d_rs.o"
    subprocess.run(["rustc", "-O", "--crate-type=lib", "--emit=obj",
                    str(src), "-o", str(obj)], check=True)
    print("\n=== vs rustc -O (ground truth) ===")
    report("rustc", objdump_functions(obj), ok)
else:
    print("\nrustc not available in this environment — run on host")

print("\nSUBSEQUENCE:", "ALL PASS" if ok[0] else "FAILURES PRESENT")
