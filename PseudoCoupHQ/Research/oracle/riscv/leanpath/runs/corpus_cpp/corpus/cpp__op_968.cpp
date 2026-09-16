// probe 968 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_968(int32_t a, uint64_t b)
{
    return a not_eq b;
}
