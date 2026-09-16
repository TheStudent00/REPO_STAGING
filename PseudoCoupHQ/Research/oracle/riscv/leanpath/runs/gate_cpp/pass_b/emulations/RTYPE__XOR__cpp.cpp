// probe 397 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_397(int64_t a, int64_t b)
{
    return a ^ b;
}


extern "C" uint64_t
emu_RTYPE__XOR(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_397(a, b));
}
