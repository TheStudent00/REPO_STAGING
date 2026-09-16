// probe 766 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_766(uint64_t a, double b)
{
    return a <=> b;
}
