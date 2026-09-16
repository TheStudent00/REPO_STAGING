// probe 927 -- binary xor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_927(bool a, float b)
{
    return a xor b;
}
