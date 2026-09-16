// probe 609 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_609(int32_t a, float b)
{
    return a <= b;
}
