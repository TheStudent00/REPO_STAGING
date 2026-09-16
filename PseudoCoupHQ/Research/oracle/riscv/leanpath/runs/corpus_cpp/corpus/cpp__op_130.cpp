// probe 130 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_130(double a, double b)
{
    return a + b;
}
