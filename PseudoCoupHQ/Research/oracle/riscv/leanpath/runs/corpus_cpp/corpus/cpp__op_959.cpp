// probe 959 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_959(double a, bool b)
{
    return a bitand b;
}
