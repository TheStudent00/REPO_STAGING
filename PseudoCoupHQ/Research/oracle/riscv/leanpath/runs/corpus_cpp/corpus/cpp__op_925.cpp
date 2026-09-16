// probe 925 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_925(bool a, int64_t b)
{
    return a xor b;
}
