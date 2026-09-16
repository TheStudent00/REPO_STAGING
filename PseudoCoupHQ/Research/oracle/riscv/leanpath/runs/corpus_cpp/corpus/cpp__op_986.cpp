// probe 986 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_986(float a, uint64_t b)
{
    return a not_eq b;
}
