// probe 426 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_426(int32_t a, int32_t b)
{
    return a & b;
}
