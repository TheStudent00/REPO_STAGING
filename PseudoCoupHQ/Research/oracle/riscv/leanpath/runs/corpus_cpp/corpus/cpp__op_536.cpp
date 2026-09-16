// probe 536 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_536(int32_t a, uint64_t b)
{
    return a > b;
}
