// probe 262 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_262(uint64_t a, double b)
{
    return a % b;
}
