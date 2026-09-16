// probe 188 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_188(uint64_t a, uint64_t b)
{
    return a * b;
}
