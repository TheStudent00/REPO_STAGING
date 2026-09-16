// probe 931 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_931(int32_t a, int64_t b)
{
    return a bitand b;
}
