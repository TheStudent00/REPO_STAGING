// probe 921 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_921(double a, float b)
{
    return a xor b;
}
