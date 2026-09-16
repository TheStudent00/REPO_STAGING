// probe 454 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_454(double a, double b)
{
    return a & b;
}
