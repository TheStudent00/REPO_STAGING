// probe 768 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_768(float a, int32_t b)
{
    return a <=> b;
}
