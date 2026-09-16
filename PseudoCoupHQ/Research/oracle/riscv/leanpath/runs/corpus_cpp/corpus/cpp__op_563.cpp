// probe 563 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_563(double a, bool b)
{
    return a > b;
}
