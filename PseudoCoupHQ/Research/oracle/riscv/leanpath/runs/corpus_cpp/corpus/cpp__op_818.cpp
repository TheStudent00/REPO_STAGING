// probe 818 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_818(bool a, uint64_t b)
{
    return a or b;
}
