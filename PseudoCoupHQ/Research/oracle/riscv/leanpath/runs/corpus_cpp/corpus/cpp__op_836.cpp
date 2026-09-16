// probe 836 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_836(uint64_t a, uint64_t b)
{
    return a and b;
}
