// probe 429 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_429(int32_t a, float b)
{
    return a & b;
}
