// probe 803 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_803(uint64_t a, bool b)
{
    return a or b;
}
