// probe 270 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_270(double a, int32_t b)
{
    return a % b;
}
