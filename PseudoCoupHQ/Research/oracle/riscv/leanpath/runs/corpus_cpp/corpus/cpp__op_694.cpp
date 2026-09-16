// probe 694 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_694(uint64_t a, double b)
{
    return a << b;
}
