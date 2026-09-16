// probe 928 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_928(bool a, double b)
{
    return a xor b;
}
