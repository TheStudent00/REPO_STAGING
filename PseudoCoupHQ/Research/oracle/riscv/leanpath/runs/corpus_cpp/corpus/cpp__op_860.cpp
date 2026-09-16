// probe 860 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_860(int32_t a, uint64_t b)
{
    return a bitor b;
}
