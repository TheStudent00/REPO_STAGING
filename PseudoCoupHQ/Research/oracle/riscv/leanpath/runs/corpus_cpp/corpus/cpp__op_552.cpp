// probe 552 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_552(float a, int32_t b)
{
    return a > b;
}
