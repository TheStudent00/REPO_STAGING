// probe 584 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_584(uint64_t a, uint64_t b)
{
    return a >= b;
}
