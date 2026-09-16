// probe 909 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_909(uint64_t a, float b)
{
    return a xor b;
}
