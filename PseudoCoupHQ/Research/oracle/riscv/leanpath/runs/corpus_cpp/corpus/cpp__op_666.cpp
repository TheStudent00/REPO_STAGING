// probe 666 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_666(double a, int32_t b)
{
    return a < b;
}
