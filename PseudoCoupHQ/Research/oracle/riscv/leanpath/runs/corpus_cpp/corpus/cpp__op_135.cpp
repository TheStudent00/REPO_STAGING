// probe 135 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_135(bool a, float b)
{
    return a + b;
}
