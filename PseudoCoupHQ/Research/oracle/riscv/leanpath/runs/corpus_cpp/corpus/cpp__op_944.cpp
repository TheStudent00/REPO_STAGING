// probe 944 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_944(uint64_t a, uint64_t b)
{
    return a bitand b;
}
