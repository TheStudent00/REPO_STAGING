// probe 624 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_624(float a, int32_t b)
{
    return a <= b;
}
