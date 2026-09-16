// probe 952 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_952(float a, double b)
{
    return a bitand b;
}
