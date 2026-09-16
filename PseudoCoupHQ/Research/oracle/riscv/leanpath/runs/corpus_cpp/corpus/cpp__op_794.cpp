// probe 794 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_794(int64_t a, uint64_t b)
{
    return a or b;
}
