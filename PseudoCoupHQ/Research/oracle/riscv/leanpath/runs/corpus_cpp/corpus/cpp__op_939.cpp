// probe 939 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_939(int64_t a, float b)
{
    return a bitand b;
}
