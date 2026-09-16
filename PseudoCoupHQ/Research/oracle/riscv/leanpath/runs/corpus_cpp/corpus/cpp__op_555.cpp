// probe 555 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_555(float a, float b)
{
    return a > b;
}
