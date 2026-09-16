// probe 699 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_699(float a, float b)
{
    return a << b;
}
