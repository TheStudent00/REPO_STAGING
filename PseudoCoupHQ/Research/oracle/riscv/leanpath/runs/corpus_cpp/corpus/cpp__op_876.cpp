// probe 876 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_876(float a, int32_t b)
{
    return a bitor b;
}
