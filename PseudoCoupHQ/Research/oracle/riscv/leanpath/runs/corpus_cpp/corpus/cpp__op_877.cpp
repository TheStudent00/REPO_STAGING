// probe 877 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_877(float a, int64_t b)
{
    return a bitor b;
}
