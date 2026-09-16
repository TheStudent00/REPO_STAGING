// probe 635 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_635(double a, bool b)
{
    return a <= b;
}
