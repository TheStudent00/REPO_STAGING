// probe 257 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_257(int64_t a, bool b)
{
    return a % b;
}
