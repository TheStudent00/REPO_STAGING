// probe 912 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_912(float a, int32_t b)
{
    return a xor b;
}
