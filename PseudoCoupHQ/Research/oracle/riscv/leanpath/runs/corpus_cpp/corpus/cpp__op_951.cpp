// probe 951 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_951(float a, float b)
{
    return a bitand b;
}
