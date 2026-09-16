// probe 346 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_346(double a, double b)
{
    return a && b;
}
