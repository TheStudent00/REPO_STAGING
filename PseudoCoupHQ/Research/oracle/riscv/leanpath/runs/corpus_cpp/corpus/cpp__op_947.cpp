// probe 947 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_947(uint64_t a, bool b)
{
    return a bitand b;
}
