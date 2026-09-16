// probe 626 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_626(float a, uint64_t b)
{
    return a <= b;
}
