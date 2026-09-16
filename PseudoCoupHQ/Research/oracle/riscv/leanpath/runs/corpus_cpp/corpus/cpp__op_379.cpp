// probe 379 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_379(double a, int64_t b)
{
    return a | b;
}
