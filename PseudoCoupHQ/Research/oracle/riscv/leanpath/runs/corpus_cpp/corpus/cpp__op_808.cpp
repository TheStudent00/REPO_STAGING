// probe 808 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_808(float a, double b)
{
    return a or b;
}
