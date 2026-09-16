// probe 591 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_591(float a, float b)
{
    return a >= b;
}
