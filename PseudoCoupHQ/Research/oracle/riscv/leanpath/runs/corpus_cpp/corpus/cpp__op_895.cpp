// probe 895 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_895(int32_t a, int64_t b)
{
    return a xor b;
}
