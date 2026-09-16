// probe 589 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_589(float a, int64_t b)
{
    return a >= b;
}
