// probe 217 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_217(int64_t a, int64_t b)
{
    return a / b;
}


extern "C" uint64_t
emu_DIV__false(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_217(a, b));
}
