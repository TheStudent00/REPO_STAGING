// probe 789 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_789(int32_t a, float b)
{
    return a or b;
}
