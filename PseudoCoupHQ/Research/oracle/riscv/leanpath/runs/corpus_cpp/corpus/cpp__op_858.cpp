// probe 858 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_858(int32_t a, int32_t b)
{
    return a bitor b;
}
