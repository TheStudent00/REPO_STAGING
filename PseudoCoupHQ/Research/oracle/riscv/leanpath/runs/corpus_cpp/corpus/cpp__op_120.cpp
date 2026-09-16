// probe 120 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_120(float a, int32_t b)
{
    return a + b;
}
