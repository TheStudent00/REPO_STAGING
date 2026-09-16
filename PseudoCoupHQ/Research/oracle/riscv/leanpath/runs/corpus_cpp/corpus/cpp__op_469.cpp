// probe 469 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_469(int64_t a, int64_t b)
{
    return a == b;
}
