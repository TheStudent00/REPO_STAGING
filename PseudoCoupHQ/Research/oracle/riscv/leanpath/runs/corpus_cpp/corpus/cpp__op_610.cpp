// probe 610 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_610(int32_t a, double b)
{
    return a <= b;
}
