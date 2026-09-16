// probe 414 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_414(double a, int32_t b)
{
    return a ^ b;
}
