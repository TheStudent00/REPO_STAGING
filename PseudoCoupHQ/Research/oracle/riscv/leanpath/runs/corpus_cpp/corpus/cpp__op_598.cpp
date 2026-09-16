// probe 598 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_598(double a, double b)
{
    return a >= b;
}
