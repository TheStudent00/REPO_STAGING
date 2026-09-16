// probe 678 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_678(int32_t a, int32_t b)
{
    return a << b;
}


extern "C" uint64_t
emu_RTYPEW__SLLW(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_678(a, b));
}
