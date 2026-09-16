// probe 934 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_934(int32_t a, double b)
{
    return a bitand b;
}
