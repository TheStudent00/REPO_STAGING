// probe 278 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_278(bool a, uint64_t b)
{
    return a % b;
}
