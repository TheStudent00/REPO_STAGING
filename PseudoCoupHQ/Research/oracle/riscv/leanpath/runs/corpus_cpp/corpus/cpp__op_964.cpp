// probe 964 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_964(bool a, double b)
{
    return a bitand b;
}
