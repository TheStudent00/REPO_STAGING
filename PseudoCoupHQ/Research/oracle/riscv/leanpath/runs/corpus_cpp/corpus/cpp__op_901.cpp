// probe 901 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_901(int64_t a, int64_t b)
{
    return a xor b;
}
