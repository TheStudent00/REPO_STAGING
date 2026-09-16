// probe 123 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_123(float a, float b)
{
    return a + b;
}
