// probe 124 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_124(float a, double b)
{
    return a + b;
}
