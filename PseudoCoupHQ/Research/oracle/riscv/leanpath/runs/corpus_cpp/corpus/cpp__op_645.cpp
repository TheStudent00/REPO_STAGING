// probe 645 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_645(int32_t a, float b)
{
    return a < b;
}
