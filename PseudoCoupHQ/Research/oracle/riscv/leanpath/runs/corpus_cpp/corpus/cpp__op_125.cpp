// probe 125 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_125(float a, bool b)
{
    return a + b;
}
