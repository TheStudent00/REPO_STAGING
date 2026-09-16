// probe 849 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_849(double a, float b)
{
    return a and b;
}
