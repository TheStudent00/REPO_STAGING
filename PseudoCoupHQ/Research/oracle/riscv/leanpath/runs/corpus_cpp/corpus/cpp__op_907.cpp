// probe 907 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_907(uint64_t a, int64_t b)
{
    return a xor b;
}
