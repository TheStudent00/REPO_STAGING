// probe 267 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_267(float a, float b)
{
    return a % b;
}
