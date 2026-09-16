// probe 279 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_279(bool a, float b)
{
    return a % b;
}
