// probe 847 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_847(double a, int64_t b)
{
    return a and b;
}
