// probe 705 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_705(double a, float b)
{
    return a << b;
}
