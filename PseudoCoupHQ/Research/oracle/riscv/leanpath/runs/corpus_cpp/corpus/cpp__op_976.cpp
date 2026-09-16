// probe 976 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_976(int64_t a, double b)
{
    return a not_eq b;
}
