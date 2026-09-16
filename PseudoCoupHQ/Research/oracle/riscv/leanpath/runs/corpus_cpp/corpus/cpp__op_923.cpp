// probe 923 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_923(double a, bool b)
{
    return a xor b;
}
