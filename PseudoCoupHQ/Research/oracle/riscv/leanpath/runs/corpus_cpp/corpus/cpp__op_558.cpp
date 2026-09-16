// probe 558 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_558(double a, int32_t b)
{
    return a > b;
}
