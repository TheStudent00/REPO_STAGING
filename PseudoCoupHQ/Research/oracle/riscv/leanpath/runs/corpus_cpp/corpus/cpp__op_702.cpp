// probe 702 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_702(double a, int32_t b)
{
    return a << b;
}
