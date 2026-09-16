// probe 946 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_946(uint64_t a, double b)
{
    return a bitand b;
}
