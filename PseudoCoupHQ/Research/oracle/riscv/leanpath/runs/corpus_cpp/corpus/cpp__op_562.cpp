// probe 562 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_562(double a, double b)
{
    return a > b;
}
