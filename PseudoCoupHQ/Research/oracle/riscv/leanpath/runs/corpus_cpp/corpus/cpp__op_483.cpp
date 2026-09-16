// probe 483 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_483(float a, float b)
{
    return a == b;
}
