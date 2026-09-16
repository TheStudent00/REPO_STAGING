// probe 248 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_248(int32_t a, uint64_t b)
{
    return a % b;
}
