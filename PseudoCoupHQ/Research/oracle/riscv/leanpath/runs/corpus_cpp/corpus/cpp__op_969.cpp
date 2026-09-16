// probe 969 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_969(int32_t a, float b)
{
    return a not_eq b;
}
