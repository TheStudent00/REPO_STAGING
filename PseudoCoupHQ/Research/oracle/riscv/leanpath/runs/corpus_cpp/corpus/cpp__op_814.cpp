// probe 814 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_814(double a, double b)
{
    return a or b;
}
