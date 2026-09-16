// probe 366 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_366(uint64_t a, int32_t b)
{
    return a | b;
}
