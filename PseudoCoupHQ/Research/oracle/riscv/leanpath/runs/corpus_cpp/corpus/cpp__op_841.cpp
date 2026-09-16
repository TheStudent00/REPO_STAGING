// probe 841 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_841(float a, int64_t b)
{
    return a and b;
}
