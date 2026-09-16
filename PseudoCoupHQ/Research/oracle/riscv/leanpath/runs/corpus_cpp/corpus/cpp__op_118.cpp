// probe 118 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_118(uint64_t a, double b)
{
    return a + b;
}
