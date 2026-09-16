// probe 455 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_455(double a, bool b)
{
    return a & b;
}
