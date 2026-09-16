// probe 972 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_972(int64_t a, int32_t b)
{
    return a not_eq b;
}
