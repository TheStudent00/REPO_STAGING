// probe 590 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_590(float a, uint64_t b)
{
    return a >= b;
}
