// probe 578 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_578(int64_t a, uint64_t b)
{
    return a >= b;
}
