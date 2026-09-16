// probe 256 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_256(int64_t a, double b)
{
    return a % b;
}
