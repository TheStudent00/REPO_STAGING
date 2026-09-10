"""Settled acceptance of the T6 INSERTION increment; no PCv5 artifact on the pass/fail path.

Everything is tested against HAND-SUPPLIED byte sequences written here
from the Intel SDM encoding rules (see BYTES below), and ground truth is
computed in-test (truncating division), never harvested from PCv5.

Acceptance (CORE at PRIVATE/PseudoCoup_v6/Planning/node_0_0_tools/
node_0_0_5_slicer/node_0_0_5_2_insertion/CORE_0_0_5_2_insertion.md):
(a) mounting the signed idiv+cqto stub and calling it computes truncating
    division: -7 idiv 2 -> -3, where Python's -7//2 floors to -4 (the
    recorded divergence, the headline test);
(b) a grid of signed/unsigned/extremes/-1-divisor inputs matches
    in-test truncating-division ground truth;
(c) a deliberately wrong platform assertion (aarch64) REFUSES to mount;
(d) the typed border cell refuses unqualified operators; int(x) crosses;
(e) page accounting: N mounts -> N live pages; closing releases to 0;
(f) the insertion cache holds pages for process life and a plan change
    invalidates (closes + re-mounts) the stale page.

Run:
    python3 -m pytest PRIVATE/PseudoIR/Tools/insert/test_insertion.py -q
"""

import ctypes
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import mount_bytes as mb                 # noqa: E402
import insertion_cache as ic             # noqa: E402
import cross_border as cb                # noqa: E402


# ---------------------------------------------------------------------------
# HAND-SUPPLIED byte fixtures, written from the Intel SDM Vol.2 encoding
# rules. Both stubs take (i64 a in RDI, i64 b in RSI) and return in RAX
# (System V AMD64). ModRM byte = (mod<<6)|(reg<<3)|(rm), mod=0b11
# register-direct; RAX=0, RDX=2, RSI=6, RDI=7.
# ---------------------------------------------------------------------------

# Signed truncating division  RAX = RDI idiv RSI:
#   48 89 F8   MOV rax, rdi     (89 /r; reg=RDI(7) rm=RAX(0) -> C0|38|00 = F8)
#   48 99      CQO              (sign-extend RAX into RDX:RAX; REX.W+99)
#   48 F7 FE   IDIV rsi         (F7 /7; reg=/7 rm=RSI(6) -> C0|38|06 = FE)
#   C3         RET
IDIV_STUB = bytes([0x48, 0x89, 0xF8, 0x48, 0x99, 0x48, 0xF7, 0xFE, 0xC3])

# Unsigned division  RAX = RDI div RSI:
#   48 89 F8   MOV rax, rdi
#   31 D2      XOR edx, edx     (zero RDX; canonical high-dividend clear)
#   48 F7 F6   DIV rsi          (F7 /6; reg=/6 rm=RSI(6) -> C0|30|06 = F6)
#   C3         RET
DIV_STUB = bytes([0x48, 0x89, 0xF8, 0x31, 0xD2, 0x48, 0xF7, 0xF6, 0xC3])

I64_MIN, I64_MAX = -(1 << 63), (1 << 63) - 1
U64_MAX = (1 << 64) - 1


def trunc_div(a, b):
    """Truncating (toward-zero) integer division: in-test ground truth."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


# --------------------------------------------------------------------------
# (a) the headline divergence
# --------------------------------------------------------------------------

def test_divergence_headline():
    m = mb.mount(IDIV_STUB)
    try:
        observed = m.call(-7, 2)
        assert observed == -3            # truncating: toward zero
        assert observed != (-7 // 2)     # Python floors to -4 -- the divergence
        assert (-7 // 2) == -4
    finally:
        m.close()


# --------------------------------------------------------------------------
# (b) the signed / unsigned / extremes / -1-divisor grid
# --------------------------------------------------------------------------

def test_signed_grid_matches_truncating_ground_truth():
    m = mb.mount(IDIV_STUB, sig=mb.FN2)
    try:
        # divisors never 0 (hardware #DE); MIN/-1 excluded (see note below).
        signed_inputs = [
            (-7, 2), (7, 2), (-7, -2), (7, -2),
            (0, 5), (0, -5), (1, 1), (-1, 1), (1, -1), (-1, -1),
            (100, 7), (-100, 7), (100, -7), (-100, -7),
            (I64_MAX, 3), (I64_MIN, 3), (I64_MAX, -3), (I64_MIN, -3),
            (I64_MAX, 1), (I64_MIN, 1),
            (I64_MAX, I64_MAX), (I64_MIN, I64_MIN),
            (12345, -1), (-9999, -1), (I64_MAX, -1),  # -1 divisor (safe: not MIN)
        ]
        for a, b in signed_inputs:
            assert m.call(a, b) == trunc_div(a, b), (a, b)
    finally:
        m.close()


def test_signed_MIN_over_neg1_is_a_hardware_trap_not_mounted():
    # IDIV(MIN, -1) raises #DE (SIGFPE) in hardware -- executing it would
    # crash the process. The polyfill traps it as OverflowError; that is
    # the ground truth, verified WITHOUT executing the mounted stub.
    from wrap_fixed_width import I64  # T4 reuse
    with pytest.raises(OverflowError):
        I64(I64_MIN) // I64(-1)


def test_unsigned_grid_matches_ground_truth():
    m = mb.mount(DIV_STUB, sig=mb.FN2U)
    try:
        unsigned_inputs = [
            (7, 2), (100, 7), (0, 5), (1, 1),
            (U64_MAX, 3), (U64_MAX, U64_MAX), (U64_MAX, 1),
            (U64_MAX - 1, 2), (1 << 63, 2), ((1 << 63) + 1, 2),
        ]
        for a, b in unsigned_inputs:
            assert m.call(a, b) == (a // b), (a, b)   # unsigned: floor == trunc
    finally:
        m.close()


# --------------------------------------------------------------------------
# (c) wrong platform assertion refuses to mount
# --------------------------------------------------------------------------

def test_wrong_arch_refuses_to_mount():
    baseline = mb.live_pages()
    with pytest.raises(mb.MountRefused):
        mb.mount(IDIV_STUB, target=mb.MountTarget(arch="aarch64"))
    assert mb.live_pages() == baseline           # nothing was mounted


def test_wrong_os_and_unsupported_cc_refuse():
    with pytest.raises(mb.MountRefused):
        mb.mount(IDIV_STUB, target=mb.MountTarget(os_family="windows"))
    with pytest.raises(mb.MountRefused):
        mb.mount(IDIV_STUB, target=mb.MountTarget(calling_convention="win64"))


def test_correct_target_mounts():
    m = mb.mount(IDIV_STUB, target=mb.MountTarget())   # x86-64 / sysv / posix
    try:
        assert m.call(9, 4) == 2
    finally:
        m.close()


def test_empty_and_oversized_bytes_refused():
    with pytest.raises(mb.MountRefused):
        mb.mount(b"")
    with pytest.raises(mb.MountRefused):
        mb.mount(b"\x90" * 5000)


# --------------------------------------------------------------------------
# (d) the typed border cell
# --------------------------------------------------------------------------

def test_border_cell_refuses_unqualified_operators():
    m = mb.mount(IDIV_STUB)
    try:
        c = cb.cell(m.call(-7, 2))
        assert isinstance(c, cb.BorderCell)
        assert int(c) == -3                    # outbound crossing: explicit, allowed
        for op in (lambda: c + 1, lambda: 1 + c, lambda: c * 2,
                   lambda: c // 2, lambda: c % 2, lambda: -c,
                   lambda: c & 1, lambda: c << 1):
            with pytest.raises(TypeError):
                op()
    finally:
        m.close()


def test_border_cell_range_check():
    with pytest.raises(OverflowError):
        cb.cell(1 << 63)                       # outside i64
    assert int(cb.cell(I64_MIN)) == I64_MIN
    assert int(cb.cell(I64_MAX)) == I64_MAX


# --------------------------------------------------------------------------
# (e) page accounting
# --------------------------------------------------------------------------

def test_page_accounting_mount_and_release():
    baseline = mb.live_pages()
    mounts = [mb.mount(IDIV_STUB) for _ in range(5)]
    assert mb.live_pages() == baseline + 5     # N mounts -> N live pages
    for m in mounts:
        m.close()
    assert mb.live_pages() == baseline          # closing releases to baseline (0 delta)


def test_double_close_is_idempotent():
    baseline = mb.live_pages()
    m = mb.mount(IDIV_STUB)
    assert mb.live_pages() == baseline + 1
    m.close()
    m.close()                                   # second close must not double-decrement
    assert mb.live_pages() == baseline


# --------------------------------------------------------------------------
# (f) the insertion cache
# --------------------------------------------------------------------------

def test_cache_holds_and_reuses():
    baseline = mb.live_pages()
    cache = ic.InsertionCache()
    try:
        a = cache.get_or_mount("Div", "rust", ("i64", "i64"), "planA", IDIV_STUB)
        b = cache.get_or_mount("Div", "rust", ("i64", "i64"), "planA", IDIV_STUB)
        assert a is b                           # same plan -> held page reused
        assert cache.live() == 1
        assert mb.live_pages() == baseline + 1
        assert a.call(-7, 2) == -3
    finally:
        cache.close_all()
    assert mb.live_pages() == baseline


def test_cache_plan_change_invalidates():
    baseline = mb.live_pages()
    cache = ic.InsertionCache()
    try:
        a = cache.get_or_mount("Div", "rust", ("i64", "i64"), "planA", IDIV_STUB)
        assert cache.plan_for("Div", "rust", ("i64", "i64")) == "planA"
        b = cache.get_or_mount("Div", "rust", ("i64", "i64"), "planB", IDIV_STUB)
        assert b is not a                       # plan changed -> re-mounted
        assert cache.plan_for("Div", "rust", ("i64", "i64")) == "planB"
        assert cache.live() == 1                # slot replaced, not leaked
        assert mb.live_pages() == baseline + 1  # stale page was released
    finally:
        cache.close_all()
    assert mb.live_pages() == baseline
