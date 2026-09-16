// probe 116 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_116(uint64_t a, uint64_t b)
{
    return a + b;
}


extern "C" uint64_t
emu_RTYPE__ADD(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_116(a, b));
}
