// probe 914 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_914(float a, uint64_t b)
{
    return a xor b;
}
