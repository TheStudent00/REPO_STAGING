// probe 917 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_917(float a, bool b)
{
    return a xor b;
}
