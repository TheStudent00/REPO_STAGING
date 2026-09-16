// probe 896 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_896(int32_t a, uint64_t b)
{
    return a xor b;
}
