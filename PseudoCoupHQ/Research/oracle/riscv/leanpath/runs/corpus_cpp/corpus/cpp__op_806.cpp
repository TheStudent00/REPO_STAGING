// probe 806 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_806(float a, uint64_t b)
{
    return a or b;
}
