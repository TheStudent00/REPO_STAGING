// probe 494 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_494(bool a, uint64_t b)
{
    return a == b;
}
