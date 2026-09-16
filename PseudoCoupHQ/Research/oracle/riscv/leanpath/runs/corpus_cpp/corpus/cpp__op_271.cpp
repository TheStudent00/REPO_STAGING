// probe 271 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_271(double a, int64_t b)
{
    return a % b;
}
