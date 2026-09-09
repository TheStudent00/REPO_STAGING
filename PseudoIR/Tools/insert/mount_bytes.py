"""Mount machine-code bytes as a callable, with platform assumptions asserted at mount time.

PROVENANCE (harvested, not invented):
  The four-step mount (mmap READ|WRITE PRIVATE|ANON -> memmove -> mprotect
  READ|EXEC -> ctypes.CFUNCTYPE) and the page-owning `MountedCode`
  (close() munmaps; __del__ defensively closes) are ported from
  PseudoCoup_v5/Research/rust_routing/output_ring.py
  (67 lines, read-and-verified). That module is the proven mechanism.

ADDED in PCv6 (what PCv5 left implicit, marked as inferred/new):
  - Platform assumptions (x86-64, System V AMD64 RDI/RSI in / RAX out,
    POSIX mmap/mprotect) are DECLARED as a `MountTarget` and ASSERTED
    against the running host at mount time; a mismatch REFUSES to mount
    (raises MountRefused) rather than executing wrong code.
  - Byte-length / non-empty invariants asserted before any executable
    page is created (never mount unvalidated or empty input).
  - Page accounting: live mounted pages are counted (`live_pages()`);
    close() releases; a leak is therefore countable.

SECURITY: mounts executable memory. Bytes must be hand-supplied fixtures
or harvested-proven sequences only; platform + length invariants are
asserted here, never bypassed.
"""

import ctypes
import ctypes.util
import mmap
import os
import platform
from dataclasses import dataclass

# --- libc bindings (ported verbatim from output_ring.py) ---
_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
_libc.mmap.restype = ctypes.c_void_p
_libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                       ctypes.c_int, ctypes.c_int, ctypes.c_long]
_libc.mprotect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
_libc.munmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t]

PROT_READ, PROT_WRITE, PROT_EXEC = 1, 2, 4
MAP_PRIVATE, MAP_ANONYMOUS = 0x02, 0x20

# (i64, i64) -> i64, System V AMD64: first two int args RDI/RSI, return RAX.
FN2 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64)
# unsigned variant for u64 stubs (same ABI, different ctypes marshalling).
FN2U = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)

# Reasonable ceiling for a hand-supplied arithmetic stub; refuses giant blobs.
_MAX_CODE_BYTES = 4096


class MountRefused(RuntimeError):
    """Raised when a declared platform assumption does not match the host,
    or a byte-invariant fails, so no executable page is ever created."""


@dataclass(frozen=True)
class MountTarget:
    """The platform assumptions a byte sequence was produced for, DECLARED
    so they can be asserted (PCv5 hard-coded these; here they fail loudly).

    arch                 canonical CPU arch the bytes encode for
    calling_convention   integer-arg/return ABI the stub obeys
    os_family            syscall family the mount path needs
    """

    arch: str = "x86-64"
    calling_convention: str = "sysv_amd64"   # RDI, RSI in; RAX out
    os_family: str = "posix"


# Host arch spellings normalized to the canonical token used above.
_ARCH_ALIASES = {
    "x86_64": "x86-64", "x86-64": "x86-64", "amd64": "x86-64",
    "aarch64": "aarch64", "arm64": "aarch64",
}

# The only ABI this mount path knows how to marshal (RDI/RSI in, RAX out).
_SUPPORTED_CC = {"sysv_amd64"}


def _host_target() -> MountTarget:
    """What the running machine actually is (inferred from platform/os)."""
    arch = _ARCH_ALIASES.get(platform.machine().lower(), platform.machine().lower())
    os_family = "posix" if os.name == "posix" else os.name
    # On POSIX x86-64 the C ABI IS System V AMD64; that is the ABI the
    # ctypes CFUNCTYPE marshalling below assumes.
    cc = "sysv_amd64" if (arch == "x86-64" and os_family == "posix") else "unknown"
    return MountTarget(arch=arch, calling_convention=cc, os_family=os_family)


def assert_target(declared: MountTarget) -> None:
    """Refuse (raise) unless the declared assumptions match the host.

    Checked BEFORE any page is mmapped, so a wrong assertion never leads
    to wrong code executing."""
    host = _host_target()
    if declared.calling_convention not in _SUPPORTED_CC:
        raise MountRefused(
            f"unsupported calling convention {declared.calling_convention!r}; "
            f"this mount path marshals only {sorted(_SUPPORTED_CC)}")
    mism = []
    if declared.arch != host.arch:
        mism.append(f"arch declared {declared.arch!r} but host is {host.arch!r}")
    if declared.os_family != host.os_family:
        mism.append(f"os declared {declared.os_family!r} but host is {host.os_family!r}")
    if declared.calling_convention != host.calling_convention:
        mism.append(f"calling-convention declared {declared.calling_convention!r} "
                    f"but host provides {host.calling_convention!r}")
    if mism:
        raise MountRefused(
            "platform assertion mismatch, refusing to mount (would execute "
            "wrong code): " + "; ".join(mism))


# --- page accounting (new in PCv6) ---
_LIVE_PAGES = 0


def live_pages() -> int:
    """How many mounted executable pages are currently live (unclosed)."""
    return _LIVE_PAGES


class MountedCode:
    """An executable page holding machine code, plus a callable view; owns its page."""

    def __init__(self, code: bytes, sig=FN2, target: MountTarget = MountTarget()):
        if not isinstance(code, (bytes, bytearray)) or len(code) == 0:
            raise MountRefused("refusing to mount empty / non-bytes code")
        if len(code) > _MAX_CODE_BYTES:
            raise MountRefused(
                f"refusing to mount {len(code)} bytes (> {_MAX_CODE_BYTES} cap); "
                f"hand-supplied stubs only")
        assert_target(target)                       # refuse before any page exists
        code = bytes(code)

        size = max(mmap.PAGESIZE, (len(code) + mmap.PAGESIZE - 1)
                   // mmap.PAGESIZE * mmap.PAGESIZE)
        addr = _libc.mmap(None, size, PROT_READ | PROT_WRITE,
                          MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)
        if not addr or addr == ctypes.c_void_p(-1).value:
            raise OSError(ctypes.get_errno(), "mmap failed")
        ctypes.memmove(addr, code, len(code))
        if _libc.mprotect(ctypes.c_void_p(addr), size,
                          PROT_READ | PROT_EXEC) != 0:
            err = ctypes.get_errno()
            _libc.munmap(ctypes.c_void_p(addr), size)
            raise OSError(err, "mprotect failed")

        self._addr, self._size, self._len = addr, size, len(code)
        self.target = target
        self.call = sig(addr)
        global _LIVE_PAGES
        _LIVE_PAGES += 1

    def __repr__(self):
        return (f"<MountedCode {self._len} bytes @ 0x{self._addr:x} "
                f"{self.target.arch}/{self.target.calling_convention}>")

    def close(self):
        if self._addr:
            _libc.munmap(ctypes.c_void_p(self._addr), self._size)
            self._addr = None
            self.call = None
            global _LIVE_PAGES
            _LIVE_PAGES -= 1

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass


def mount(code: bytes, sig=FN2, target: MountTarget = MountTarget()) -> MountedCode:
    """Mount a hand-supplied/proven byte sequence into a callable executable page."""
    return MountedCode(code, sig, target)
