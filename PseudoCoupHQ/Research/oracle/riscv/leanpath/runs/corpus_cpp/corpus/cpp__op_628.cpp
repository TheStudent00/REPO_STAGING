// probe 628 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_628(float a, double b)
{
    return a <= b;
}
