// probe 940 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_940(int64_t a, double b)
{
    return a bitand b;
}
