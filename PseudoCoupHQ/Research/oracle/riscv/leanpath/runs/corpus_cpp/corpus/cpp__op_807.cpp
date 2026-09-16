// probe 807 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_807(float a, float b)
{
    return a or b;
}
