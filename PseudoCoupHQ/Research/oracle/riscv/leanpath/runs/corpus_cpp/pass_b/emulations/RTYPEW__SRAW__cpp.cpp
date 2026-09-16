// probe 714 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_714(int32_t a, int32_t b)
{
    return a >> b;
}


extern "C" uint64_t
emu_RTYPEW__SRAW(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_714(a, b));
}
