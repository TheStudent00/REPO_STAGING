// probe 962 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_962(bool a, uint64_t b)
{
    return a bitand b;
}
