// probe 700 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_700(float a, double b)
{
    return a << b;
}
