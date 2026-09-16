// probe 340 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_340(float a, double b)
{
    return a && b;
}
