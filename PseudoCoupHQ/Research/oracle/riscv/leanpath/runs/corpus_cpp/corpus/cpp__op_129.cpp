// probe 129 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_129(double a, float b)
{
    return a + b;
}
