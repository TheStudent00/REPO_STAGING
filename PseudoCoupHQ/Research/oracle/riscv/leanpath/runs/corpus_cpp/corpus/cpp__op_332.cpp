// probe 332 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_332(uint64_t a, uint64_t b)
{
    return a && b;
}
