// probe 898 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_898(int32_t a, double b)
{
    return a xor b;
}
