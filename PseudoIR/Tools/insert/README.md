# T6 — Slicer (INSERTION increment)

The SELECTION and EXTRACTION increments of this tool (`select_slices.py`,
`extract_slices.py` and their co-modules, persisted plans, and extracted
modules) were built pointing at a retired reference backend instead of at
the settled LLVM/rustc-LLVM direction. the owner ordered them purged
(2026-07-30): removed as mis-aimed, not carried forward. No claim from
that work stands. The forward direction for slicing compiler sources is
LLVM/rustc-LLVM; a future SELECTION/EXTRACTION increment will be rebuilt
against that target when a form declares it.

Status: INSERTION mount+border+cache+platform-assertion core done
(`node_0_0_5_2_*`); this is the only increment of this node currently
present in the repo.

# INSERTION increment

Mounts machine-code bytes so hub Python can call them, crosses the
result back through a typed border, and caches the mounted page.
Governing settled node:
`<WORKSPACE_DIR>/PseudoIR/Planning/node_0_0_tools/node_0_0_2_insert/SUPPORT_insertion.md`.
This increment is the mount + border + cache + platform-assertion core
tested against a HAND-SUPPLIED byte sequence (the known x86-64
idiv+cqto stub); it does not perform the lowering/encoding
byte-extraction (that depends on a SELECTION/EXTRACTION increment not
currently present in this repo — see above), and it carries the `.pc`
import-hook surface / CPython-fork question forward UNCHANGED per the
CORE's default.

## Files

| file | role |
|---|---|
| `mount_bytes.py` | harvest of PCv5 `output_ring.py`: libc `mmap` (READ\|WRITE, PRIVATE\|ANON) -> `memmove` -> `mprotect` (READ\|EXEC) -> `ctypes.CFUNCTYPE`; `MountedCode` owns its page (`close()` munmaps, `__del__` defensively closes). ADDS a DECLARED `MountTarget` (arch / calling-convention / os) asserted at mount time — a mismatch raises `MountRefused` before any page exists — plus `live_pages()` accounting and byte-length invariants |
| `cross_border.py` | harvest of PCv5 `rust_cell.py`: a `BorderCell` that refuses every unqualified Python operator; outward crossing is explicit `int(x)`. Reuses (imports, does not copy) the T4 polyfill `I64` for the i64 range check |
| `insertion_cache.py` | cache keyed by (intention, language, type-tuple, PLAN-IDENTITY) from the PCv5 `pc_runtime.py`/`ledger.py` (operation,type) dispatch pattern; holds pages for process life; a changed plan-identity closes and re-mounts the stale page. `live()` / `live_pages()` make lifetime measurable |
| `test_insertion.py` | the settled acceptance (14 tests), PCv5-free: the `-7 idiv 2 -> -3` divergence, the signed/unsigned/extremes/`-1`-divisor grid vs in-test truncating ground truth, the aarch64 refusal, the border cell, page accounting, and cache plan-invalidation |
| `README.md` | this file |

## The mounted byte sequence (Intel SDM Vol.2, written by hand)

Signed truncating division, System V AMD64 (a in RDI, b in RSI, result
in RAX):

| bytes | instruction | note |
|---|---|---|
| `48 89 F8` | `MOV rax, rdi` | 89 /r; ModRM reg=RDI(7) rm=RAX(0) -> 0xF8 |
| `48 99` | `CQO` | sign-extend RAX into RDX:RAX (REX.W + 99) |
| `48 F7 FE` | `IDIV rsi` | F7 /7; ModRM reg=/7 rm=RSI(6) -> 0xFE |
| `C3` | `RET` | |

The full stub is `48 89 F8 48 99 48 F7 FE C3`. The headline test mounts
it and observes `call(-7, 2) == -3` (x86 IDIV truncates toward zero),
where Python's `-7 // 2` floors to `-4` — the recorded divergence. An
unsigned `DIV` stub (`48 89 F8 31 D2 48 F7 F6 C3`) covers the unsigned
grid.

## Platform assertion (declared, not assumed)

The PCv5 hard-coded assumptions (x86-64, System V AMD64, POSIX
`mmap`/`mprotect`) are a `MountTarget` asserted against the running host
at mount time. Declaring `arch="aarch64"` (or `calling_convention=
"win64"`, or `os_family="windows"`) on this host raises `MountRefused`
before any executable page is created — a wrong assertion refuses to
mount, it never executes wrong code.

## Honest gaps (marked, not faked)

- `IDIV(MIN, -1)` and any zero divisor raise a hardware `#DE`/SIGFPE
  that would crash the process; they are NOT executed through the
  mounted stub. Their ground truth (a trap) is asserted via the T4
  polyfill's `OverflowError` instead.
- Polyfill reconciliation: the border DISTINGUISHES its operator policy
  from `FixedWidthInt` (this cell REFUSES bare operators; there the
  operator IS the routing) but REUSES polyfill `I64` for the range
  definition — reuse-of-arithmetic + distinct-border, not duplication.

## Run

```bash
python3 -m pytest <WORKSPACE_DIR>/PseudoIR/Tools/insert/ -q
```
