// probe 919 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_919(double a, int64_t b)
{
    return a xor b;
}
