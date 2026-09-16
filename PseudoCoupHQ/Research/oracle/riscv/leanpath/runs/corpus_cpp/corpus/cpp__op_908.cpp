// probe 908 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_908(uint64_t a, uint64_t b)
{
    return a xor b;
}
