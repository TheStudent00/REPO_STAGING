// probe 358 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_358(int32_t a, double b)
{
    return a | b;
}
