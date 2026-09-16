// probe 795 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_795(int64_t a, float b)
{
    return a or b;
}
