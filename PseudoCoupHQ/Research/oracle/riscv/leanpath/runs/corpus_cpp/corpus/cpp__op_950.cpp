// probe 950 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_950(float a, uint64_t b)
{
    return a bitand b;
}
