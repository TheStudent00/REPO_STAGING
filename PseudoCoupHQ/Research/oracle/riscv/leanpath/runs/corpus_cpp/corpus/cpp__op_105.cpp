// probe 105 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_105(int32_t a, float b)
{
    return a + b;
}
