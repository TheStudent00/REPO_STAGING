// probe 141 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_141(int32_t a, float b)
{
    return a - b;
}
