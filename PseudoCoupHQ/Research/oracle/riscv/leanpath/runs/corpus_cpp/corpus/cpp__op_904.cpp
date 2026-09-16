// probe 904 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_904(int64_t a, double b)
{
    return a xor b;
}
