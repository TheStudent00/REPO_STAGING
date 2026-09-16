// probe 787 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_787(int32_t a, int64_t b)
{
    return a or b;
}
