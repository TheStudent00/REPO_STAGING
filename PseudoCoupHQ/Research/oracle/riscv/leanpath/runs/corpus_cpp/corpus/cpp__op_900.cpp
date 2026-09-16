// probe 900 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_900(int64_t a, int32_t b)
{
    return a xor b;
}
