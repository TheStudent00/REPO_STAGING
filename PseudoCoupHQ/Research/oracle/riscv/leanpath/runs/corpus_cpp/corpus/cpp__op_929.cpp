// probe 929 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_929(bool a, bool b)
{
    return a xor b;
}
