// probe 846 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_846(double a, int32_t b)
{
    return a and b;
}
