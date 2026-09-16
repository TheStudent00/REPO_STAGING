// probe 370 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_370(uint64_t a, double b)
{
    return a | b;
}
