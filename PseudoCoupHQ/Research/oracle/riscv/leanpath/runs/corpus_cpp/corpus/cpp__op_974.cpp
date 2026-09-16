// probe 974 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_974(int64_t a, uint64_t b)
{
    return a not_eq b;
}
