// probe 411 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_411(float a, float b)
{
    return a ^ b;
}
