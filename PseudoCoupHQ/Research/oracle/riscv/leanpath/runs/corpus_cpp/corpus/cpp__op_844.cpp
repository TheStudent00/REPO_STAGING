// probe 844 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_844(float a, double b)
{
    return a and b;
}
