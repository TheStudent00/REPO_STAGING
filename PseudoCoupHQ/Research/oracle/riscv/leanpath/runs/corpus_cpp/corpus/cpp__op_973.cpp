// probe 973 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_973(int64_t a, int64_t b)
{
    return a not_eq b;
}
