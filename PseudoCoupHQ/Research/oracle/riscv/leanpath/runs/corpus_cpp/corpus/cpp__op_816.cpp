// probe 816 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_816(bool a, int32_t b)
{
    return a or b;
}
