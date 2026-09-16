// probe 408 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_408(float a, int32_t b)
{
    return a ^ b;
}
