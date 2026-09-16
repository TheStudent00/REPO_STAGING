// probe 963 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_963(bool a, float b)
{
    return a bitand b;
}
