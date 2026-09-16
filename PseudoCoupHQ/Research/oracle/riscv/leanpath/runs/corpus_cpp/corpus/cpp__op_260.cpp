// probe 260 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_260(uint64_t a, uint64_t b)
{
    return a % b;
}
