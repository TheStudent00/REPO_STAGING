// probe 663 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_663(float a, float b)
{
    return a < b;
}
