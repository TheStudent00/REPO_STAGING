// probe 887 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_887(double a, bool b)
{
    return a bitor b;
}
