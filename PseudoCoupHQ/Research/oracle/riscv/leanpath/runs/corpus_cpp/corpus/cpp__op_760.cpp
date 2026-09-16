// probe 760 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_760(int64_t a, double b)
{
    return a <=> b;
}
