// probe 572 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_572(int32_t a, uint64_t b)
{
    return a >= b;
}
