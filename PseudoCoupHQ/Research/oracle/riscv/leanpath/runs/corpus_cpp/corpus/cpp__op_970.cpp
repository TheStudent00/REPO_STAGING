// probe 970 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_970(int32_t a, double b)
{
    return a not_eq b;
}
