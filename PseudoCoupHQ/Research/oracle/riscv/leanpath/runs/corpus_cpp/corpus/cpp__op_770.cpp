// probe 770 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_770(float a, uint64_t b)
{
    return a <=> b;
}
