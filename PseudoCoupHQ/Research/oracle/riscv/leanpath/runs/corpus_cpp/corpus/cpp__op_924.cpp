// probe 924 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_924(bool a, int32_t b)
{
    return a xor b;
}
