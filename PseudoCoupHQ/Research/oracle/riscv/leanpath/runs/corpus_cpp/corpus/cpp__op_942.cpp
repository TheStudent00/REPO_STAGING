// probe 942 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_942(uint64_t a, int32_t b)
{
    return a bitand b;
}
