// probe 268 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_268(float a, double b)
{
    return a % b;
}
