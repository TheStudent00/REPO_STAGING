// probe 106 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_106(int32_t a, double b)
{
    return a + b;
}
