// probe 174 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_174(int32_t a, int32_t b)
{
    return a * b;
}


extern "C" uint64_t
emu_MULW__one(uint64_t a, uint64_t b)
{
    return (uint64_t)(op_174(a, b));
}
