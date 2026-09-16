// probe 922 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_922(double a, double b)
{
    return a xor b;
}
