// probe 534 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_534(int32_t a, int32_t b)
{
    return a > b;
}
