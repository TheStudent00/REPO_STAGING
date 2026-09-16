// probe 484 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_484(float a, double b)
{
    return a == b;
}
