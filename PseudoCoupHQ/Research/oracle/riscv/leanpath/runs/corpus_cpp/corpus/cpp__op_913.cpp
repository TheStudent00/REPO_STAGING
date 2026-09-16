// probe 913 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_913(float a, int64_t b)
{
    return a xor b;
}
