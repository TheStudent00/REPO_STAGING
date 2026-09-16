// probe 790 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_790(int32_t a, double b)
{
    return a or b;
}
