// probe 957 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_957(double a, float b)
{
    return a bitand b;
}
