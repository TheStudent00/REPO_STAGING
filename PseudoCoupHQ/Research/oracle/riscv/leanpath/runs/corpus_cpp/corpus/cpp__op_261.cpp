// probe 261 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_261(uint64_t a, float b)
{
    return a % b;
}
