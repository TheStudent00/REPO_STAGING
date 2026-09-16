// probe 375 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_375(float a, float b)
{
    return a | b;
}
