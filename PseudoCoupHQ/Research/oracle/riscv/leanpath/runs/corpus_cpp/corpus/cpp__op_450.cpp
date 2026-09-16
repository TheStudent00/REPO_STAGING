// probe 450 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_450(double a, int32_t b)
{
    return a & b;
}
