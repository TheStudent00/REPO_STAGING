// probe 903 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_903(int64_t a, float b)
{
    return a xor b;
}
