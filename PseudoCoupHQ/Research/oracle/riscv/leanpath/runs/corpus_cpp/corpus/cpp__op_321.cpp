// probe 321 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_321(int32_t a, float b)
{
    return a && b;
}
