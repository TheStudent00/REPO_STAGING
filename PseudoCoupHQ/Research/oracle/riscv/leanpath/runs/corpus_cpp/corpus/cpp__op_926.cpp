// probe 926 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_926(bool a, uint64_t b)
{
    return a xor b;
}
