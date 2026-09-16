// probe 771 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_771(float a, float b)
{
    return a <=> b;
}
