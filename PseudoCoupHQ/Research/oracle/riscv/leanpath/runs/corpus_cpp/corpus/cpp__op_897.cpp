// probe 897 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_897(int32_t a, float b)
{
    return a xor b;
}
