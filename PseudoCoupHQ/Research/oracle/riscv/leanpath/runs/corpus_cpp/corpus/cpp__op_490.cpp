// probe 490 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_490(double a, double b)
{
    return a == b;
}
