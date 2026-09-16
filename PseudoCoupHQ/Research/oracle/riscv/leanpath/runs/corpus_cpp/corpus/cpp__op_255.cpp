// probe 255 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_255(int64_t a, float b)
{
    return a % b;
}
