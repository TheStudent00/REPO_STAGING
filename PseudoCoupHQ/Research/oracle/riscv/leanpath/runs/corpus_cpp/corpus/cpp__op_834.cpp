// probe 834 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_834(uint64_t a, int32_t b)
{
    return a and b;
}
