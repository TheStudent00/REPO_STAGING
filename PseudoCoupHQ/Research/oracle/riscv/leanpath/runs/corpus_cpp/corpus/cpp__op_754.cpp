// probe 754 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_754(int32_t a, double b)
{
    return a <=> b;
}
