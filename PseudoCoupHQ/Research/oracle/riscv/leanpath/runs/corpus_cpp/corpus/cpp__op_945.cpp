// probe 945 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_945(uint64_t a, float b)
{
    return a bitand b;
}
