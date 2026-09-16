// probe 277 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_277(bool a, int64_t b)
{
    return a % b;
}
