// probe 1001 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_xor_gpr_gpr_32__primitive__cpp(bool a, bool b)
{
    return a not_eq b;
}
