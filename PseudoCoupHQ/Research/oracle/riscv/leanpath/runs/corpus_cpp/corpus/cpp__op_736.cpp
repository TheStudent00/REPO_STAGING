// probe 736 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_736(float a, double b)
{
    return a >> b;
}
