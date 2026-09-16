// probe 224 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_224(uint64_t a, uint64_t b)
{
    return a / b;
}


extern "C" uint64_t
emu_DIV__true(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_224(a, b));
}
