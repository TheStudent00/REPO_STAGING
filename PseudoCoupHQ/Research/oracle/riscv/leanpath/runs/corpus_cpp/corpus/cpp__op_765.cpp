// probe 765 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_765(uint64_t a, float b)
{
    return a <=> b;
}
