// probe 813 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_813(double a, float b)
{
    return a or b;
}
