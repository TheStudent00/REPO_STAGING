// probe 991 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_991(double a, int64_t b)
{
    return a not_eq b;
}
