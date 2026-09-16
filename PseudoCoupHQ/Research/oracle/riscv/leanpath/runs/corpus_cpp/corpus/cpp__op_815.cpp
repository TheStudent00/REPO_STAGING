// probe 815 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_815(double a, bool b)
{
    return a or b;
}
