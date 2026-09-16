// probe 802 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_802(uint64_t a, double b)
{
    return a or b;
}
