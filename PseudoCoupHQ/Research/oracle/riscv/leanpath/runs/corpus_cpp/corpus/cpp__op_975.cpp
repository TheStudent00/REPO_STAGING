// probe 975 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_975(int64_t a, float b)
{
    return a not_eq b;
}
