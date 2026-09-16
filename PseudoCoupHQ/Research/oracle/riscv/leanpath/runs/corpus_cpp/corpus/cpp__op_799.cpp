// probe 799 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_799(uint64_t a, int64_t b)
{
    return a or b;
}
