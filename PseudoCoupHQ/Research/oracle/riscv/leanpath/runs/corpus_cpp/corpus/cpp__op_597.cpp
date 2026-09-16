// probe 597 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_597(double a, float b)
{
    return a >= b;
}
