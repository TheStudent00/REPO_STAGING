// probe 153 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_153(uint64_t a, float b)
{
    return a - b;
}
