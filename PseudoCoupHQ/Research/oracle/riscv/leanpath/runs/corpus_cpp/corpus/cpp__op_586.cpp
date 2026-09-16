// probe 586 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_586(uint64_t a, double b)
{
    return a >= b;
}
