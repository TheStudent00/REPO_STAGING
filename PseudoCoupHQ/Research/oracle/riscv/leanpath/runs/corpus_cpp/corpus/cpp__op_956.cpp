// probe 956 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_956(double a, uint64_t b)
{
    return a bitand b;
}
