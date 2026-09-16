// probe 992 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_992(double a, uint64_t b)
{
    return a not_eq b;
}
