// probe 782 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_782(bool a, uint64_t b)
{
    return a <=> b;
}
