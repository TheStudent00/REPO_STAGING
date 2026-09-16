// probe 870 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_870(uint64_t a, int32_t b)
{
    return a bitor b;
}
