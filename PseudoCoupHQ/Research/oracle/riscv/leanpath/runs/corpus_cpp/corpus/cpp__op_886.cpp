// probe 886 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_886(double a, double b)
{
    return a bitor b;
}
