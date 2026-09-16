// probe 902 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_902(int64_t a, uint64_t b)
{
    return a xor b;
}
