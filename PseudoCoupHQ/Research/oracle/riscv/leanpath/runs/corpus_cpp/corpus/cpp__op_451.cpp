// probe 451 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_451(double a, int64_t b)
{
    return a & b;
}
