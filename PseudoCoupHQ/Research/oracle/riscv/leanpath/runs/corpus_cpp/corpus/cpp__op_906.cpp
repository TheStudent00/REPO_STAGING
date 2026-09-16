// probe 906 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_906(uint64_t a, int32_t b)
{
    return a xor b;
}
