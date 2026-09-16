// probe 656 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_656(uint64_t a, uint64_t b)
{
    return a < b;
}


extern "C" uint64_t
emu_RTYPE__SLTU(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_656(a, b));
}
