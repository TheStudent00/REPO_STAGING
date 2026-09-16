// probe 655 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_655(uint64_t a, int64_t b)
{
    return a < b;
}
