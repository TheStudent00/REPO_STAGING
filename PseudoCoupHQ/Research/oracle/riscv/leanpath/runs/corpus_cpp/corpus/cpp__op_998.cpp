// probe 998 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_998(bool a, uint64_t b)
{
    return a not_eq b;
}
