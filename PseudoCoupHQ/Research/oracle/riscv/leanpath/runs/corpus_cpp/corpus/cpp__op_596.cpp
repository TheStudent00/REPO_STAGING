// probe 596 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_596(double a, uint64_t b)
{
    return a >= b;
}
