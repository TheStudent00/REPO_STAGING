// probe 960 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_960(bool a, int32_t b)
{
    return a bitand b;
}
