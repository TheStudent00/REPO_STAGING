// probe 592 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_592(float a, double b)
{
    return a >= b;
}
