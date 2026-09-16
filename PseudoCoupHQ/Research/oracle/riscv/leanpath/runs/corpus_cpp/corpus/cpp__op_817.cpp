// probe 817 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_817(bool a, int64_t b)
{
    return a or b;
}
