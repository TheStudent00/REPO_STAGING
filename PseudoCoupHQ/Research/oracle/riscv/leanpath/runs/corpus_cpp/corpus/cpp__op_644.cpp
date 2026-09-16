// probe 644 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_644(int32_t a, uint64_t b)
{
    return a < b;
}
