// probe 905 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_905(int64_t a, bool b)
{
    return a xor b;
}
