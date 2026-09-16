// probe 446 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_446(float a, uint64_t b)
{
    return a & b;
}
