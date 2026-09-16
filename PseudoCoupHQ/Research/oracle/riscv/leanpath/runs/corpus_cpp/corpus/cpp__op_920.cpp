// probe 920 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_920(double a, uint64_t b)
{
    return a xor b;
}
