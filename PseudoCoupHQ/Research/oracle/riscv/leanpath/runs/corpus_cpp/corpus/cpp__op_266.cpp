// probe 266 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_266(float a, uint64_t b)
{
    return a % b;
}
