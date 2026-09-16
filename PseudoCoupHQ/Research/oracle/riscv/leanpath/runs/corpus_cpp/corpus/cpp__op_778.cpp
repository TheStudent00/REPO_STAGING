// probe 778 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_778(double a, double b)
{
    return a <=> b;
}
