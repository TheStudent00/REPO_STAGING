// probe 213 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_213(int32_t a, float b)
{
    return a / b;
}
