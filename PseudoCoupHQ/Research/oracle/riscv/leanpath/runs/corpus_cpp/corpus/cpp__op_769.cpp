// probe 769 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_769(float a, int64_t b)
{
    return a <=> b;
}
