// probe 368 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_368(uint64_t a, uint64_t b)
{
    return a | b;
}
