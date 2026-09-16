// probe 249 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_249(int32_t a, float b)
{
    return a % b;
}
