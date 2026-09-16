// probe 990 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_990(double a, int32_t b)
{
    return a not_eq b;
}
