// probe 439 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_439(uint64_t a, int64_t b)
{
    return a & b;
}
