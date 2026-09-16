// probe 342 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_342(double a, int32_t b)
{
    return a && b;
}
