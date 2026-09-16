// probe 810 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_810(double a, int32_t b)
{
    return a or b;
}
