// probe 166 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_166(double a, double b)
{
    return a - b;
}
