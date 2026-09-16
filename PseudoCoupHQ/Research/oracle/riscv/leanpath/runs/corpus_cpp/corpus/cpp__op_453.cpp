// probe 453 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_453(double a, float b)
{
    return a & b;
}
