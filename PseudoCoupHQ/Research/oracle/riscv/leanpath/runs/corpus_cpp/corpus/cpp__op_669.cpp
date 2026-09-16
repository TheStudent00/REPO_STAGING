// probe 669 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_669(double a, float b)
{
    return a < b;
}
