// probe 776 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_776(double a, uint64_t b)
{
    return a <=> b;
}
