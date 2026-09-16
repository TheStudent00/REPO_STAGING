// probe 478 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_478(uint64_t a, double b)
{
    return a == b;
}
