// probe 345 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_345(double a, float b)
{
    return a && b;
}
