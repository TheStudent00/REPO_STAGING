// probe 775 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_775(double a, int64_t b)
{
    return a <=> b;
}
