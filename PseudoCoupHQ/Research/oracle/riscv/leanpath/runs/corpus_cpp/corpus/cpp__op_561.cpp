// probe 561 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_561(double a, float b)
{
    return a > b;
}
