// probe 491 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_491(double a, bool b)
{
    return a == b;
}
