// probe 634 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_634(double a, double b)
{
    return a <= b;
}
