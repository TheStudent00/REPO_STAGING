// probe 933 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_933(int32_t a, float b)
{
    return a bitand b;
}
