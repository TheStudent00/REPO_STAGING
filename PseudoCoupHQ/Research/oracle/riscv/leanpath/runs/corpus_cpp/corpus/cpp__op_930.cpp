// probe 930 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_930(int32_t a, int32_t b)
{
    return a bitand b;
}
