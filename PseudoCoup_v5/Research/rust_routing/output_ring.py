"""Output ring: mount produced machine-code bytes and call them.

The four steps, no magic:
  1. ask the OS for a page          (mmap)
  2. write the bytes into it
  3. mark the page executable       (mprotect)
  4. call it                        (ctypes function pointer)

The bytes come from transpiled Rust routing+encoding logic. This
module never generates code; it only mounts what it is given.

Calling convention used by mounted stubs (System V AMD64):
  first two integer args in RDI, RSI; return in RAX.
"""

import ctypes
import ctypes.util
import mmap

_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
_libc.mmap.restype = ctypes.c_void_p
_libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                       ctypes.c_int, ctypes.c_int, ctypes.c_long]
_libc.mprotect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
_libc.munmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t]

PROT_READ, PROT_WRITE, PROT_EXEC = 1, 2, 4
MAP_PRIVATE, MAP_ANONYMOUS = 0x02, 0x20

# (i64, i64) -> i64
FN2 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64)


class MountedCode:
    """An executable page holding machine code, plus a callable view."""

    def __init__(self, code: bytes, sig=FN2):
        size = max(mmap.PAGESIZE, (len(code) + mmap.PAGESIZE - 1)
                   // mmap.PAGESIZE * mmap.PAGESIZE)
        addr = _libc.mmap(None, size, PROT_READ | PROT_WRITE,
                          MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)
        if not addr or addr == ctypes.c_void_p(-1).value:
            raise OSError(ctypes.get_errno(), "mmap failed")
        ctypes.memmove(addr, code, len(code))
        if _libc.mprotect(ctypes.c_void_p(addr), size,
                          PROT_READ | PROT_EXEC) != 0:
            raise OSError(ctypes.get_errno(), "mprotect failed")
        self._addr, self._size, self._len = addr, size, len(code)
        self.call = sig(addr)

    def __repr__(self):
        return f"<MountedCode {self._len} bytes @ 0x{self._addr:x}>"

    def close(self):
        if self._addr:
            _libc.munmap(ctypes.c_void_p(self._addr), self._size)
            self._addr = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass


def mount(code: bytes, sig=FN2) -> MountedCode:
    return MountedCode(code, sig)
