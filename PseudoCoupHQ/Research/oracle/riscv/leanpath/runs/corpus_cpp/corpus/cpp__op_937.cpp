// probe 937 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_937(int64_t a, int64_t b)
{
    return a bitand b;
}
