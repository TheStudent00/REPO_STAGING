// probe 982 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_982(uint64_t a, double b)
{
    return a not_eq b;
}
