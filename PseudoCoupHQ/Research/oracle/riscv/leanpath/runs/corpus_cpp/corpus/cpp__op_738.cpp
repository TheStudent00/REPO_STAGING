// probe 738 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_738(double a, int32_t b)
{
    return a >> b;
}
