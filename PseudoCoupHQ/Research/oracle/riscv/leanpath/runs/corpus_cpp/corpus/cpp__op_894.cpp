// probe 894 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_894(int32_t a, int32_t b)
{
    return a xor b;
}
