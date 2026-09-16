// probe 979 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_979(uint64_t a, int64_t b)
{
    return a not_eq b;
}
