// probe 885 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_885(double a, float b)
{
    return a bitor b;
}
