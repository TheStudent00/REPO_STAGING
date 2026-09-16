// probe 899 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_899(int32_t a, bool b)
{
    return a xor b;
}
