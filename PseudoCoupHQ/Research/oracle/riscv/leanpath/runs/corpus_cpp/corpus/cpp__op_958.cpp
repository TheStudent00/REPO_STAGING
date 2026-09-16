// probe 958 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_958(double a, double b)
{
    return a bitand b;
}
