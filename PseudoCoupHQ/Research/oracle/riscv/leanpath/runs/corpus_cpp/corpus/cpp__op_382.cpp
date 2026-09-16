// probe 382 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_382(double a, double b)
{
    return a | b;
}
