// probe 793 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_793(int64_t a, int64_t b)
{
    return a or b;
}
