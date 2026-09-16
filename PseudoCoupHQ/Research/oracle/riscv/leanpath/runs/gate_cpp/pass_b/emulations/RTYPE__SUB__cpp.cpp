// probe 146 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_146(int64_t a, uint64_t b)
{
    return a - b;
}


extern "C" uint64_t
emu_RTYPE__SUB(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_146(a, b));
}
