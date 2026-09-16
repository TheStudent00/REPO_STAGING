// probe 489 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_489(double a, float b)
{
    return a == b;
}
