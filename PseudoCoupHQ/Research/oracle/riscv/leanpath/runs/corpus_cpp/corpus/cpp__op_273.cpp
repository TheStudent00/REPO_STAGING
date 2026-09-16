// probe 273 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_273(double a, float b)
{
    return a % b;
}
