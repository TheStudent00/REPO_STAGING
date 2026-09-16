// probe 585 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_585(uint64_t a, float b)
{
    return a >= b;
}
