// probe 272 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_272(double a, uint64_t b)
{
    return a % b;
}
