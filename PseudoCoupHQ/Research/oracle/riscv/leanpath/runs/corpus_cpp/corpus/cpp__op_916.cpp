// probe 916 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_916(float a, double b)
{
    return a xor b;
}
