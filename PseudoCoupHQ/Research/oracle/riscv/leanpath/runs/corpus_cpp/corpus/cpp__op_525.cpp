// probe 525 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_525(double a, float b)
{
    return a != b;
}
