// probe 456 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_456(bool a, int32_t b)
{
    return a & b;
}
