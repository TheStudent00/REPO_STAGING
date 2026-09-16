// probe 983 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_983(uint64_t a, bool b)
{
    return a not_eq b;
}
