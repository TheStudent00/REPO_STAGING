// probe 343 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_343(double a, int64_t b)
{
    return a && b;
}
