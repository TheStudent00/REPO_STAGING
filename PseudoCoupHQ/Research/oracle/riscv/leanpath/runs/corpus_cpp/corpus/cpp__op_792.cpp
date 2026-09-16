// probe 792 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_792(int64_t a, int32_t b)
{
    return a or b;
}
