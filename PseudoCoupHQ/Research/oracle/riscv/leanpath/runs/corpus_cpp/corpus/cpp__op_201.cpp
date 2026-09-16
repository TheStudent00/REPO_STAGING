// probe 201 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_201(double a, float b)
{
    return a * b;
}
