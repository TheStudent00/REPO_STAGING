// probe 126 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_126(double a, int32_t b)
{
    return a + b;
}
