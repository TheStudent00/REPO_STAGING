// probe 798 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_798(uint64_t a, int32_t b)
{
    return a or b;
}
