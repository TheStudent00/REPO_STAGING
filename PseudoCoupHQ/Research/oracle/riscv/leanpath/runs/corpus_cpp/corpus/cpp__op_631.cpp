// probe 631 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_631(double a, int64_t b)
{
    return a <= b;
}
