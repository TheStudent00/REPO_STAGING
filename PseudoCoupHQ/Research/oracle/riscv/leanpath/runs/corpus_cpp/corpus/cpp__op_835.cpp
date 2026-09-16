// probe 835 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_835(uint64_t a, int64_t b)
{
    return a and b;
}
