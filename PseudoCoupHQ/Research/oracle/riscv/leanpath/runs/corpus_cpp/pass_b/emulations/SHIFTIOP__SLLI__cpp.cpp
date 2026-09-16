// probe 692 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_692(uint64_t a, uint64_t b)
{
    return a << b;
}


extern "C" uint64_t
emu_SHIFTIOP__SLLI(uint64_t a, uint64_t shamt)
{
    return (uint64_t)(op_692(a, shamt));
}
