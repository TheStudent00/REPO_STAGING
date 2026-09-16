// probe 254 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_254(int64_t a, uint64_t b)
{
    return a % b;
}
