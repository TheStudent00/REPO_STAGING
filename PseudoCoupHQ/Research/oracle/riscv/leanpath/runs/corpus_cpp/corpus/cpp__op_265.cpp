// probe 265 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_265(float a, int64_t b)
{
    return a % b;
}
