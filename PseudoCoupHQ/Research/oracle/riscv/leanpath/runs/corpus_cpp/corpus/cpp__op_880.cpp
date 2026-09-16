// probe 880 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_880(float a, double b)
{
    return a bitor b;
}
