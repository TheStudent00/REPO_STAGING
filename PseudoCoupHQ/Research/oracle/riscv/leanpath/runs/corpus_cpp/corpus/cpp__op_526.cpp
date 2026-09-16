// probe 526 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_526(double a, double b)
{
    return a != b;
}
