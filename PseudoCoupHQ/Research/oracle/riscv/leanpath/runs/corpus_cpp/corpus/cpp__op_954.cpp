// probe 954 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_954(double a, int32_t b)
{
    return a bitand b;
}
