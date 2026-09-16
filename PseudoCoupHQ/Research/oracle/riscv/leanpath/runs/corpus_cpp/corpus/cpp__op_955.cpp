// probe 955 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_955(double a, int64_t b)
{
    return a bitand b;
}
