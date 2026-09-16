// probe 786 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_786(int32_t a, int32_t b)
{
    return a or b;
}
