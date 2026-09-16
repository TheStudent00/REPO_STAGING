// probe 753 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_753(int32_t a, float b)
{
    return a <=> b;
}
