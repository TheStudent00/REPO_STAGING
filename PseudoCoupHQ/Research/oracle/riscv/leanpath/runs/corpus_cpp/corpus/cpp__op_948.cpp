// probe 948 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_948(float a, int32_t b)
{
    return a bitand b;
}
