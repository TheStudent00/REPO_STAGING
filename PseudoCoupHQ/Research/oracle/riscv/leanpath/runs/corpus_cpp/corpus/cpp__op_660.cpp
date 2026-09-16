// probe 660 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_660(float a, int32_t b)
{
    return a < b;
}
