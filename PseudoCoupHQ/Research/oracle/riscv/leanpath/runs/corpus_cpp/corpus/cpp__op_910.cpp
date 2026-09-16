// probe 910 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_910(uint64_t a, double b)
{
    return a xor b;
}
