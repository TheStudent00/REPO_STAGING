// probe 911 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_911(uint64_t a, bool b)
{
    return a xor b;
}
