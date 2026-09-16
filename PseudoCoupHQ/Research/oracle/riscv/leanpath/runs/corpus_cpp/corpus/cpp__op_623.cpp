// probe 623 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_623(uint64_t a, bool b)
{
    return a <= b;
}
