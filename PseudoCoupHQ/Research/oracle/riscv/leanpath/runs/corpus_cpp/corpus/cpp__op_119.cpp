// probe 119 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_119(uint64_t a, bool b)
{
    return a + b;
}
