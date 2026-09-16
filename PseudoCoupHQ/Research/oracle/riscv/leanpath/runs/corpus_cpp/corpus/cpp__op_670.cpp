// probe 670 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_670(double a, double b)
{
    return a < b;
}
