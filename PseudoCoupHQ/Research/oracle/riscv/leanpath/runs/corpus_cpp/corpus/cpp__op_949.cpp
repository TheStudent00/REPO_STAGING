// probe 949 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_949(float a, int64_t b)
{
    return a bitand b;
}
