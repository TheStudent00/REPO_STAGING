// probe 915 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_915(float a, float b)
{
    return a xor b;
}
