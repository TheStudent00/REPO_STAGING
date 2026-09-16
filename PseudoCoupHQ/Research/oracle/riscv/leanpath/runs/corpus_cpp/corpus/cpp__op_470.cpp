// probe 470 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_470(int64_t a, uint64_t b)
{
    return a == b;
}
