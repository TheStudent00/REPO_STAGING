// probe 622 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_622(uint64_t a, double b)
{
    return a <= b;
}
