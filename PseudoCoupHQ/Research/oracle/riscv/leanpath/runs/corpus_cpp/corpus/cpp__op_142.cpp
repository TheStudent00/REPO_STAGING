// probe 142 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_142(int32_t a, double b)
{
    return a - b;
}
