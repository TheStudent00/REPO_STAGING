// probe 918 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_918(double a, int32_t b)
{
    return a xor b;
}
