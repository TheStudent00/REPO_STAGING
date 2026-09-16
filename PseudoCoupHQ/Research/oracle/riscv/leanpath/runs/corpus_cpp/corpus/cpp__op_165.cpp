// probe 165 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_165(double a, float b)
{
    return a - b;
}
