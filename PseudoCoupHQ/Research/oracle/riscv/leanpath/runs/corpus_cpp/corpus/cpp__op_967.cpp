// probe 967 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_967(int32_t a, int64_t b)
{
    return a not_eq b;
}
