// probe 250 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_250(int32_t a, double b)
{
    return a % b;
}
